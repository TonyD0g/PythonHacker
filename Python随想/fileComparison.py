# 找出在A文件中但不在B文件中的内容（A - B）
import sys


def find_unique_lines(fileA_path, fileB_path, ignore_case=False, ignore_blank=False, output_file=None):
    """
    找出在A文件中但不在B文件中的内容（A - B）

    参数:
        fileA_path: A文件路径
        fileB_path: B文件路径
        ignore_case: 是否忽略大小写 (默认False)
        ignore_blank: 是否忽略空行 (默认False)
        output_file: 结果输出文件路径 (默认None，输出到终端)
    """
    try:
        # 读取A文件内容
        with open(fileA_path, 'r', encoding='utf-8') as fileA:
            if ignore_blank:
                linesA = [line.rstrip('\n') for line in fileA if line.strip()]
            else:
                linesA = [line.rstrip('\n') for line in fileA]

        # 读取B文件内容
        with open(fileB_path, 'r', encoding='utf-8') as fileB:
            if ignore_blank:
                linesB = {line.rstrip('\n') for line in fileB if line.strip()}
            else:
                linesB = {line.rstrip('\n') for line in fileB}

        # 处理大小写选项
        if ignore_case:
            linesB = {line.lower() for line in linesB}
            unique_lines = [line for line in linesA if line.lower() not in linesB]
        else:
            unique_lines = [line for line in linesA if line not in linesB]

        # 输出结果
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as out:
                for line in unique_lines:
                    out.write(line + '\n')
            print(f"结果已保存至: {output_file}")
            print(f"在A中但不在B中的行数: {len(unique_lines)}")
        else:
            if unique_lines:
                print("在A中但不在B中的内容:")
                for i, line in enumerate(unique_lines, 1):
                    print(f"{line}")
                print(f"\n总计: {len(unique_lines)} 行")
            else:
                print("A中没有B中不存在的内容")

        return unique_lines

    except FileNotFoundError as e:
        print(f"文件错误: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"处理错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    # 解析命令行参数
    fileA = '/Users/macmini/Downloads/a.txt'
    fileB = '/Users/macmini/Downloads/b.txt'
    ignore_case = False
    ignore_blank = False
    output_file = None

    if '--ignore-case' in sys.argv:
        ignore_case = True
    if '--ignore-blank' in sys.argv:
        ignore_blank = True
    if '--output' in sys.argv:
        try:
            output_index = sys.argv.index('--output') + 1
            output_file = sys.argv[output_index]
        except IndexError:
            print("错误: --output 参数后需指定输出文件路径")
            sys.exit(1)

    find_unique_lines(fileA, fileB, ignore_case, ignore_blank, output_file)
