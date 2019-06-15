import hashlib

# obj = hashlib.md5(b"jflkasdjklfjaskljfdfjdsakljfklajslfjaskljfklasjklasj")  # 加盐
# obj.update("123456".encode("utf-8"))  # 把要加密的内容给md5
print(hashlib.md5(b"jflkasdjklfjaskljfdfjdsakljfklajslfjaskljfkcclasjklasj").hexdigest())
