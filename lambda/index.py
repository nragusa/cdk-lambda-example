import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    try:
        # ======Check and turn on Detailed Monitoring where required======
        ec2_con=boto3.client("ec2")
        non_mon_ids=[]
        f1={"Name": "monitoring-state", "Values":['disabled']}
        for each_in in ec2_con.describe_instances(Filters=[f1])['Reservations']:
            for each_item in each_in['Instances']:
                non_mon_ids.append(each_item['InstanceId'])
        print("Turning on Detailed Monitoring for ids: ",non_mon_ids)
        ec2_con.monitor_instances(InstanceIds=non_mon_ids)
    except ClientError as error:
        print(error)
    except Exception as e:
        print(e) 
