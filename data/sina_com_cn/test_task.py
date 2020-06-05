from .task import *

def get_stock_list_test():
    task = get_stock_list.s(None,{
        "num":40,
        "sort":"symbol",
        "asc":1,
        "node":"sh_a",
        "symbol":"",
        "_s_r_a":"page",
    },{"NAME":"stock","PREFIX":"sina_a","INDEX":["symbol"]})
    print(task.apply_async().get())

    # task = get_stock_list_data.s(None,{
    #     "num":40,
    #     "page":1,
    #     "sort":"symbol",
    #     "asc":1,
    #     "node":"sh_a",
    #     "symbol":"",
    #     "_s_r_a":"page",
    # })
    # print(task.apply_async().get())

def main():
    get_stock_list_test()

if __name__ == "__main__":
    main()