# def test(arr, target):
#     # return list(filter(lambda ele: [target - ele == item for item in arr if item != ele], arr))
#     def is_valid(ele, arr, target):
#         for item in arr:
#             if target - ele == item:
#                 return item
#     return list(filter(lambda ele: is_valid(ele, [item for item in arr if item != ele], target), arr))
#
# print(test([1, 2, 4, 6, 7, 9], 9))
