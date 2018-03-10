#Author: Samson oni(soni5@umbc.edu, www.samdwise.com)
import boto3
import configparser

class CreateRource:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('configuration.ini')
        ##################Launch Configuration parameters ##########################
        self.launch_config_name = config['LaunchConfiguration']['Name']
        self.ami_id = config['LaunchConfiguration']['Ami_Id']
        self.instanceType = config['LaunchConfiguration']['InstanceType']
        self.keyPair = config['LaunchConfiguration']['KeyPair']
        self.securityGroup = self.convertToNoneType(config['LaunchConfiguration']['SecurityGroup'])
        self.public_ip = self.convertToBoolean(config['LaunchConfiguration']['PublicIp'])
        self.user_data = self.convertToNoneType(config['LaunchConfiguration']['UserData'])
        self.cluster = self.convertToNoneType(config['LaunchConfiguration']['Cluster'])

        ####################AutoScaling group parameters##########################
        self.autoscaling_name = config['AutoScalingGroup']['Name']
        self.minSize = int(config['AutoScalingGroup']['MinSize'])
        self.maxSize = int(config['AutoScalingGroup']['MaxSize'])
        self.desiredSize = int(config['AutoScalingGroup']['DesiredSize'])
        self.availabilityZones = config['AutoScalingGroup']['AvailabilityZones']
        self.subnets = self.convertToNoneType(config['AutoScalingGroup']['Subnets'])

        ###################Elastic Load Balancer parameters#######################
        self.elb_name = config['ELB']['Name']
        self.protocol = config['ELB']['Protocol']
        self.elb_port = int(config['ELB']['ELBPort'])
        self.instance_port = int(config['ELB']['InstancePort'])
        self.ssl_certificate = config['ELB']['SSLCertificate']
        self.subnets = self.convertToNoneType(config['ELB']['Subnets'])
        self.private = self.convertToBoolean(config['ELB']['Private'])

        ##################Redis parameters######################################
        self.elastic_name = config['Redis']['Name']
        self.elastic_available_zones = config['Redis']['PreferredAvailabilityZone']
        self.numCacheNodes = int(config['Redis']['NumCacheNodes'])
        self.engine = config['Redis']['Engine']
        self.cache_node_type = config['Redis']['CacheNodeType']


######################################################################################################
    '''Below function is to create client session that will be used for all needed services'''
    def boto_session(self,resource):
        client_session = boto3.Session()
        return client_session.client(resource)
#################################################################################################
    def create_launch_configuration(self):
        client = self.boto_session("autoscaling")
        parameter = {}
        parameter["LaunchConfigurationName"] = self.launch_config_name
        parameter["ImageId"] = self.ami_id
        parameter["InstanceType"] = self.instanceType
        if self.keyPair != 'None':
            parameter["KeyName"] = self.keyPair
        if self.securityGroup :
            parameter["SecurityGroups"] = self.securityGroup
        if self.public_ip:
            parameter["AssociatePublicIpAddress"] = True
        if self.cluster != 'None':
            parameter["UserData"] = "#!/bin/bash\n" \
                                 + "echo ECS_CLUSTER=" \
                                 + self.launch_config_name \
                                 + " >> /etc/ecs/ecs.config"
        elif self.user_data:
            parameter["UserData"] = self.user_data
        return client.create_launch_configuration(**parameter)

######################################################################################
    """Creating auto scale group with the launch configuration"""
    def create_auto_scaling_group(self):
        client = self.boto_session('autoscaling')
        parameters = {}
        parameters["AutoScalingGroupName"] = self.autoscaling_name
        parameters["LaunchConfigurationName"] = self.launch_config_name
        parameters["MinSize"] = self.minSize
        parameters["MaxSize"] = self.maxSize
        parameters["DesiredCapacity"] = self.desiredSize
        parameters["AvailabilityZones"] = [self.availabilityZones]
        if self.subnets:
            parameters["VPCZoneIdentifier"] = ",".join(self.subnets)
        return client.create_auto_scaling_group(**parameters)

##################################################################################################
    """Create an Elastic load balancer"""
    def create_elastic_load_balancer(self):
        elb_client = self.boto_session('elb')
        parameters = {}
        parameters["LoadBalancerName"] = self.elb_name
        parameters["AvailabilityZones"] = [self.availabilityZones]
        listener = {
                 "Protocol": self.protocol,
                 "LoadBalancerPort": self.elb_port,
                 "InstancePort": self.instance_port
                 }
        if self.ssl_certificate:
            listener["SSLCertificateId"] = self.ssl_certificate
        parameters['Listeners'] = [listener]

        if self.subnets:
            parameters['Subnets'] = self.subnets
        if self.securityGroup:
            parameters["SecurityGroups"] = self.securityGroup
        if self.private:
            parameters['Scheme'] = 'internal'
        return elb_client.create_load_balancer(**parameters)
###########################################################################################

    """Attach load balacer to autoscaling group"""
    def attach_load_balacer_to_autoscaling(self):
        attach_client = self.boto_session('autoscaling')
        parameters = {}
        parameters['AutoScalingGroupName'] = self.autoscaling_name
        parameters['LoadBalancerNames'] = [self.elb_name]
        return attach_client.attach_load_balancers(**parameters)

    ################################################################################

    """Create Elasticache cluster"""
    ###############################################################################
    def create_elasticache_cluster(self):
        client = self.boto_session('elasticache')
        parameters = {}
        parameters["CacheClusterId"] = self.elastic_name
        parameters["PreferredAvailabilityZone"] = self.elastic_available_zones
        parameters["NumCacheNodes"] = self.numCacheNodes
        parameters['Engine'] = self.engine
        parameters['CacheNodeType'] = self.cache_node_type
        return client.create_cache_cluster(**parameters)


   #############################################################################
    """Functions to convert string to Nonetype"""
    def convertToNoneType(self,value):
        if value == 'None':
            return None
        return value

    """Function to convert string to boolean"""
    def convertToBoolean(self,value):
        if value == 'False':
            return False
        return True
#######################################################################################

########################################################################################
"""Invoking the creation functions. Note: The order for invoking must be preserved"""
try:
    invoke_creation = CreateRource()
    print('\n===========Creating Launch Configuration===============================\n')
    print(invoke_creation.create_launch_configuration())
    print('\n============Creating Autoscaling group==============================\n')
    print(invoke_creation.create_auto_scaling_group())
    print('\n============Creating Load balancer==============================\n')
    print(invoke_creation.create_elastic_load_balancer())
    print('\n=============Attaching Load balancer to Autoscaling========================\n')
    print(invoke_creation.attach_load_balacer_to_autoscaling())
    print('\n=============Creating Elasticache cluster========================\n')
    print(invoke_creation.create_elasticache_cluster())
except Exception as e:
    print(e)