import json

# event引数
# --------------------------------------------
# event引数にはJSON文字列がパース済みの状態で渡される
# どういったデータが含まれるかはイベント次第
# CloudWatchイベントでは、event引数の中身を任意に指定可能

def lambda_handler(event, context):
    
    print('Hello')
    print(json.dumps(event))
    
    return {
        'statusCode': 200,
    }