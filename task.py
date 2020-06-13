#task.py
import boto3

def main():
  print("Running task...")
  client = boto3.client('sts')
  response = client.get_caller_identity()
  print(response)

main()
