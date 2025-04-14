import boto3
import socket

def get_aws_account_info():
    """Retrieve AWS account information."""
    sts = boto3.client('sts')
    identity = sts.get_caller_identity()
    account_id = identity['Account']
    return account_id

def get_ec2_public_ips():
    """Retrieve public IP addresses from EC2 instances."""
    ec2 = boto3.client('ec2')
    public_ips = []

    # Describe all EC2 instances
    response = ec2.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if 'PublicIpAddress' in instance:
                public_ips.append(instance['PublicIpAddress'])

    return public_ips

def get_elb_public_ips():
    """Retrieve public IP addresses from Elastic Load Balancers."""
    elb = boto3.client('elb')
    public_ips = []

    # Describe all classic load balancers
    response = elb.describe_load_balancers()
    for load_balancer in response['LoadBalancerDescriptions']:
        dns_name = load_balancer['DNSName']
        try:
            # Resolve DNS name to IP address
            ip_address = socket.gethostbyname(dns_name)
            public_ips.append(ip_address)
        except socket.gaierror:
            print(f"Could not resolve DNS name: {dns_name}")

    return public_ips

def get_elbv2_public_ips():
    """Retrieve public IP addresses from Application/Network Load Balancers."""
    elbv2 = boto3.client('elbv2')
    public_ips = []

    # Describe all load balancers
    response = elbv2.describe_load_balancers()
    for load_balancer in response['LoadBalancers']:
        if load_balancer['Scheme'] == 'internet-facing':
            dns_name = load_balancer['DNSName']
            try:
                # Resolve DNS name to IP address
                ip_address = socket.gethostbyname(dns_name)
                public_ips.append(ip_address)
            except socket.gaierror:
                print(f"Could not resolve DNS name: {dns_name}")

    return public_ips

def main():
    """Main function to extract all public IPs."""
    # Get AWS account information
    account_id = get_aws_account_info()
    print(f"AWS Account ID: {account_id}")

    all_public_ips = []

    # Get public IPs from EC2 instances
    ec2_ips = get_ec2_public_ips()
    all_public_ips.extend(ec2_ips)

    # Get public IPs from Classic Load Balancers
    elb_ips = get_elb_public_ips()
    all_public_ips.extend(elb_ips)

    # Get public IPs from Application/Network Load Balancers
    elbv2_ips = get_elbv2_public_ips()
    all_public_ips.extend(elbv2_ips)

    # Print all public IPs
    print(f"Public IP addresses in the AWS account ({account_id}):")
    for ip in all_public_ips:
        print(ip)

if __name__ == "__main__":
    main()
