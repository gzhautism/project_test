# -*- encoding: utf-8 -*-
# @File    : case_generate.py
# @Contact : chengcheng@heading.loc
# @Modify Time : 2021/12/29 14:17
# @Author : chengchengy
# @Version : 1.0
# @Description : 生成用例集合

def generate(excel, start_row, idlist=[], exclude=[], col = 2):
    """
    @param excel:  输入Excel对象
    @param idlist: 目前实现的是根据用例id进行选择部分用例测试
    @param exclude:排除第多少行，内容是excel中的行数，可以为列表
    @param row: 需要对比的列数默认为第二列的protocolid
    @return: 返回实际需要测试的多少行

    """
    generate_list = []
    max_rows = excel.rows
    for r in range(start_row, max_rows + 1):
        if r in exclude:
            continue
        if idlist:
            if excel.get_cell_value(r, col) in idlist:
                generate_list.append(r)
        else:
            generate_list.append(r)
    return generate_list


if __name__ == "__main__":
    from lib.Excel.operate_excel import Excel

    test_excel = Excel(file_path=r"D:\AutoTest\TestCase\AIDL\HMI_v1.0.5测试用例.xlsx", sheet_name="自动化")
    print(test_excel.rows)
    print(test_excel.cols)
    print(generate(test_excel))
