import pulumi
import pulumi_aws as aws


class Ec2_instance(pulumi.ComponentResource):
    def __init__(self,
    resource_name = str,
    ami = None,
    instance_type = None ,
    availability_zone = None,
    disable_api_termination="True",
    iam_instance_profile = None,
    key_name = None,
    cidr_blocks = ["0.0.0.0/0"],
    instance_initiated_shutdown_behavior="Stop",
    security_group = ["None"],
    user_data = None,
    subnet_id = None,
    vpc_id = "vpc-0183b5a3f116ffca8",
    ebs_volume_size = 1,
    ebs_volume_id = "Old",
    opts = None):
        self.resource_name = resource_name
        self.ami = ami
        self.key_name = key_name
        self.subnet_id = subnet_id
        self.security_group = security_group
        self.disable_api_termination = disable_api_termination
        self.instance_initiated_shutdown_behavior = instance_initiated_shutdown_behavior
        self.instance_type = instance_type
        self.iam_instance_profile = iam_instance_profile
        self.availability_zone = availability_zone
        self.cidr_blocks = cidr_blocks
        self.vpc_id = vpc_id
        self.user_data = user_data 
        self.ebs_volume_size = ebs_volume_size
        self.ebs_volume_id = ebs_volume_id
        self.opts = opts

        for i in security_group:
            if i == "New":
                securitygroup = aws.ec2.SecurityGroup("allowTls",
                    description="Allow https inbound traffic",
                    vpc_id = self.vpc_id,
                    ingress=[aws.ec2.SecurityGroupIngressArgs(
                        description="https from VPC",
                        from_port=443,
                        to_port=443,
                        protocol="tcp",
                        cidr_blocks=self.cidr_blocks,           
            )],
            egress=[aws.ec2.SecurityGroupEgressArgs(
                from_port=0,
                to_port=0,
                protocol="-1",
                cidr_blocks=["0.0.0.0/0"],
                ipv6_cidr_blocks=["::/0"],
            )],)
            else:
                securitygroup = aws.ec2.get_security_group(name=i)
               
        web = aws.ec2.Instance(f"{self.resource_name}",
            ami=self.ami,
            instance_type = self.instance_type,
            availability_zone = self.availability_zone,
            vpc_security_group_ids  = [securitygroup.id],
            disable_api_termination = self.disable_api_termination,
            user_data  = self.user_data,
            key_name = self.key_name,
            #instance_initiated_shutdown_behavior = self.instance_initiated_shutdown_behavior,

            tags={
            "Name": f"{self.resource_name}",
                 })

        if ebs_volume_id == "New":
            ebs_volume = aws.ebs.Volume("example",
                availability_zone=f"{self.availability_zone}",
                    size=self.ebs_volume_size)
        else:    
            ebs_volume = aws.ebs.get_volume(id = ebs_volume_id)

        ebs_att = aws.ec2.VolumeAttachment("ebsAtt",
            device_name="/dev/sdh",
            volume_id = ebs_volume.id,
            instance_id = web.id)