import pulumi
import pulumi_aws as aws

class Iam_user(pulumi.ComponentResource):
    def __init__(self,
    user,
    inlinepolicy={"None":"None"},
    groupname=["None"],
    login_profile = "No",
    policy=["None"],
    Access_key = "NO",
    opts = pulumi.ResourceOptions(protect=True),):
        
        self.user = user
        self.groupname = groupname
        self.policy=policy
        self.login_profile = login_profile
        self.inlinepolicy = inlinepolicy
        self.Access_key = Access_key
        self.opts = opts
        try:
            get_user = aws.iam.get_user(user_name=self.user)
            try:
                for p in self.policy:
                    policy = aws.iam.get_policy(name=p)
                    test_attach = aws.iam.UserPolicyAttachment(f"{p}",
                        user = example_user.name,
                        policy_arn=policy.arn
                    )
            except:pass
            try:
                for i,j in self.inlinepolicy.items():
                    test_attach = aws.iam.UserPolicy(f"{i}",
                        name = f"{i}",
                        user = get_user.user_name,
                        policy = (lambda path:open(path).read())(f"{j}"))
            except:pass
            try:            
                for g in self.groupname:
                    group = aws.iam.get_group(group_name=g)
                    team1 = aws.iam.UserGroupMembership(f"{g}",
                        user=example_user.name,
                    groups=[
                        group.group_name])
            except:pass

            if login_profile == "Yes":   
                    user_login_profile = aws.iam.UserLoginProfile(f"{self.user}Profile",
                        user=example_user.name,
                        password_length = 40,
                        password_reset_required=True)

            if Access_key == "Yes":
                    access_key = aws.iam.AccessKey("AccessKey", user=example_user.name,pgp_key="keybase:atom1992")
       
        except Exception as e:
            example_user = aws.iam.User(self.user,
                    name = self.user,
                    path="/",
                    force_destroy=True,
                    )
            for p in self.policy:        
                policy = aws.iam.get_policy(name=p)
                test_attach = aws.iam.UserPolicyAttachment(f"{p}",opts=pulumi.ResourceOptions(protect=True),
                            user = example_user.name,
                            policy_arn=policy.arn)

            if login_profile == "Yes":   
                    user_login_profile = aws.iam.UserLoginProfile(f"{self.user}Profile",
                        user=example_user.name,
                        password_length = 40,
                        password_reset_required=True)
            if Access_key == "Yes":
                    access_key = aws.iam.AccessKey("AccessKey", user=example_user.name,pgp_key="keybase:atom1992")
                    pulumi.export("Secretkey", access_key.encrypted_secret)            
            try:
                for g in self.groupname:
                    group = aws.iam.get_group(group_name=g)
                    team1 = aws.iam.UserGroupMembership(f"{g}",
                        user=example_user.name,
                    groups=[
                        group.group_name])
            except:pass
            try:
                for i,j in self.inlinepolicy.items():
                    test_attach = aws.iam.UserPolicy(f"{i}",
                        name = f"{i}",
                        user = get_user.user_name,
                        policy = (lambda path:open(path).read())(f"{j}"))
            except:pass
            pulumi.export("User", example_user.name)
            pulumi.export("Password", user_login_profile.password)

