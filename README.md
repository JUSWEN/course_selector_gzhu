# 广州大学gzhu抢课脚本

> 适用于广大新版教务系统 <https://newcas.gzhu.edu.cn/cas/login?service=https%3A%2F%2Fnewmy.gzhu.edu.cn%2Fup%2F>
>
> 谨献给745宿舍全体靓仔，祝各位靓仔学业顺利
>
> 邮箱 lihao_deng@qq.com
>
> 本人不对因使用此脚本而产生的任何后果或损失负责

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [广州大学gzhu抢课脚本](#广州大学gzhu抢课脚本)
  - [运行环境](#运行环境)
    - [需要安装的库](#需要安装的库)
  - [使用此脚本的教程](#使用此脚本的教程)

<!-- /code_chunk_output -->

## 不想安装python环境的同学，可以查看我的另一个github项目

[exe版广州大学gzhu抢课脚本](https://github.com/MILK2077/exe_gzhu_course_selector)

## 运行环境

python 3.9

### 需要安装的库

requests

selenium4.0.0及以上
（注意selenium3会报错）

os

用如下代码安装(如果安装不了，请自行百度):

```cmd
pip3 install requests
pip3 install selenium
pip3 install os
```

如果想使用anaconda ，请自行百度

## 使用此脚本的教程

1. 转到`edge://settings/help` 查看你的Microsoft Edge版本。
![1.png](assets/1.png)
2. 访问["Microsoft Edge驱动程序"。](https://developer.microsoft.com/microsoft-edge/tools/webdriver)

3. 在**页面的"获取**最新版本"部分，找到与你的Microsoft Edge的版本编号相匹配的，然后选择其x64版本并下载。
![2.png](assets/2.png)
4. 下载完成后，将可执行 `msedgedriver.exe` 文件放到任意位置,并添加到环境变量。

   ```powershell
   打开开始菜单->我的电脑（或计算机）->系统属性->高级系统设置->环境变量，编辑用户变量里的path， 在最后面添加（仅供参考，添加时应该添加自己的msedgedriver.exe所在的路径） ;C:\Program Files (x86)\msedgedriver.exe 或者在最前面添加 C:\Program Files (x86)\msedgedriver.exe; 总之变量之间用分号隔开，修改完之后点击确定按钮保存配置。
   ```

5. 在自己的浏览器登录教务系统选课界面，找到所有自己想选的课程，并完整复制其名称

   如图所示，示例:(130101303)学术研究与交流 - 1.0 学分
   ![3](assets/3.png)
   注意！不要把两边的空格复制进去！从"("开始复制，到"学分"的"分"字结束。

   可以把课程名称先保存在txt文件中，方便后面运行程序时复制粘贴。

   因为运行脚本时如果使用浏览器登录自己的教务系统账号，脚本的登录状态将会失效。

   同时需要记住该门课程的类别：是主修课程，板块课体育，通识选修还是其他特殊课程？需要记住。

6. 运行run.py程序。

7. 根据提示输入学号和密码
![4](assets/4.png)
![5](assets/5.png)

8. 等待一段时间，出现提示后，根据提示操作。

9. 请在选课开始前几天，选课系统试运行的时候，提前运行一次脚本录入信息,以方便在抢课开始时迅速开始抢课。

10. 请在正式选课开始前5到6分钟时使用一次脚本，以更新cookie。

11. 然后在正式选课开始时前一分钟运行脚本进行抢课。

12. 请不要随意删除程序文件夹内的文件。
