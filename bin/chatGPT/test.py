from yuan_api.inspurai import Yuan, set_yuan_account,Example

set_yuan_account("allen", "18805841931")
yuan = Yuan(input_prefix="对话：“",
            input_suffix="”",
            output_prefix="答：“",
            output_suffix="”",)
# 3. add examples if in need.
yuan.add_example(Example(inp="对百雅轩798艺术中心有了解吗？",
                        out="有些了解，它位于北京798艺术区，创办于2003年。"))

prompt = "故宫的珍宝馆里有什么好玩的？"
response = yuan.submit_API(prompt=prompt,trun="”")

print(response)