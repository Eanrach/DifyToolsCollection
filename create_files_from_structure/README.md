# 插件信息
Plugin Name : Structured File Creation
Author : Eanrach
Type : tool
Repository : https://github.com/Eanrach/DifyToolsCollection/tree/main/create_files_from_structure
# 使用说明
## 输入格式
工具接受以下格式的输入：

```json
{
    {
      "file_structure": [
        "path/to/file1.py",
        "path/to/file2.txt"
      ],
      "files": [
        {
          "filename": "path/to/file1.py",
          "content": "print('Hello World')"
        },
        {
          "filename": "path/to/file2.txt",
          "content": "This is a text file"
        }
      ]
    }
}
```

