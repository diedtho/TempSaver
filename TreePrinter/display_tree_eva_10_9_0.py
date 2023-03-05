from directory_tree import display_tree

# Main Method
if __name__ == '__main__':
    #dir_path = 'G:\\APPS\\EvaServer\\Bin_10_9_0_e'
    dir_path = r'G:\APPS\EvaServer\Bin_10_9_0_e'
    display_tree(dir_path, max_depth=2)
    stringRepresentation = display_tree(dir_path, string_rep=True, show_hidden=False, max_depth=2)
    with open('eva_tree.txt', 'w', encoding='utf8') as fw:
        fw.write(stringRepresentation)