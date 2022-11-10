import os
import subprocess

app2 = []
app1 = []

def get_label(path_exe):
    global app2
    global app1
    directory_list = os.listdir(path_exe)
    for i in directory_list:
        if os.path.isdir(i):
            new_cd = path_exe+'/'+i
            new_dir = os.listdir(new_cd)
            if 'apps.py' in new_dir:
                datam = open(new_cd+'/apps.py', 'r')
                label_line = datam.readlines()
                for mt in label_line:
                    if 'label' in mt:
                        label_dom = mt
                if 'label' in label_dom:
                    label = label_dom.strip().split('=')[-1]
                    label = label.replace('"','')
                    label = label.replace("'",'')
                    if 'app2' in label:
                        app2.append(label.strip())
                    else:
                        app1.append(label.strip())
            else:
                if 'migrations' not in new_dir or '__pycache__' not in new_dir:
                    for j in new_dir:
                        again_new_path = new_cd+'/'+j
                        if os.path.isdir(again_new_path):
                            get_label(again_new_path)
        elif 'apps.py' == i:
            new_cd = path_exe+'/'+i
            datam = open(new_cd, 'r')
            label_line = datam.readlines()
            for mt in label_line:
                if 'label' in mt:
                    label_dom = mt
            if 'label' in label_dom:
                label = label_dom.strip().split('=')[-1]
                label = label.replace('"','')
                label = label.replace("'",'')
                if 'app2' in label:
                    app2.append(label.strip())
                else:
                    app1.append(label.strip())

    return app1, app2


if __name__ == '__main__':
    cwd = os.getcwd()
    a = get_label(cwd)
    for i in a:
        if app1 == i:
            print(app1)
            for j in i:
                subprocess.Popen(['python','/home/girishparate/test_girish/testpro/manage.py','migrate',j,'--database=test_pro1'], stdout=subprocess.PIPE).communicate()
        elif app2 == i:
            print(app2)
            for j in i:
                subprocess.Popen(['python','/home/girishparate/test_girish/testpro/manage.py','migrate',j,'--database=test_pro2'], stdout=subprocess.PIPE).communicate()
        else:
            pass