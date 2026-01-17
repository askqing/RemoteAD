@echo off
echo 测试脚本执行正常！
echo 当前目录: %cd%
echo 选择项测试:
echo 1. 测试选项1
echo 2. 测试选项2
echo.
set /p choice=请输入选项 (1-2): 

if %choice%==1 (
    echo 您选择了选项1
) else if %choice%==2 (
    echo 您选择了选项2
) else (
    echo 无效选项
)

echo 测试完成！
pause