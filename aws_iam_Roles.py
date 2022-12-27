import pulumi
import pulumi_aws as aws

class Iam_Role(pulumi.ComponentResource):
    def __init__(self,
    role,
    policy=["None"],
    inlinepolicy= {"None":"None"},
    InstanceProfile = "No",
    trust_relationship = None,
    opts = pulumi.ResourceOptions(protect=True),):
        self.role = role
        self.policy= policy
        self.inlinepolicy = inlinepolicy
        self.InstanceProfile = InstanceProfile
        self.trust_relationship = trust_relationship
        
        try:
            get_role = aws.iam.get_role(user_name=self.role)
            try:            
                for p in self.policy:
                    policy = aws.iam.get_policy(name=p)
                    test_attach = aws.iam.RolePolicyAttachment(f"{p}",
                        role = role.name,
                        policy_arn=policy.arn
                    )
            except:pass
            try:
                for i,j in self.inlinepolicy.items():
                    test_policy = aws.iam.RolePolicy(f"{i}",
                        name = f"{i}",
                        role=role.id,
                        policy=(lambda path:open(path).read())(f"{j}")
                        )
            except:pass
            if InstanceProfile == "Yes":
                profile = aws.iam.InstanceProfile(f"{self.role}",name = f"{self.role}",role=role.name)
            pulumi.export("role", role.id)

        except Exception as e:
            role = aws.iam.Role(f"{self.role}", 
                        name=f"{self.role}",
                        assume_role_policy=(lambda path:open(path).read())(f"{self.trust_relationship}"))
            try:            
                for p in self.policy:
                    policy = aws.iam.get_policy(name=p)
                    test_attach = aws.iam.RolePolicyAttachment(f"{p}",
                        role = role.name,
                        policy_arn=policy.arn
                    )
            except:pass
            try:
                for i,j in self.inlinepolicy.items():
                    test_policy = aws.iam.RolePolicy(f"{i}",
                        name = f"{i}",
                        role=role.id,
                        policy=(lambda path:open(path).read())(f"{j}")
                        )
            except:pass
            if InstanceProfile == "Yes":
                profile = aws.iam.InstanceProfile(f"{self.role}",name = f"{self.role}",role=role.name)
                    
            pulumi.export("role", role.id)

