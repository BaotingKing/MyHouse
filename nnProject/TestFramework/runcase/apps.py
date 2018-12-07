from django.apps import AppConfig


class RuncaseConfig(AppConfig):
    name = 'runcase'

def fun():
    new = {'two': 2}
    return new


if __name__ == '__main__':
    temp = {'one': 1}
    temp.update(fun())
    amp = dict(
                style='errorClass',
                desc='desc',
                count=100,
                Pass=100,
                fail=0,
                error=0,
                cid='c%s' % (1 + 1),)
    amp = bool('a' or '')
    print(temp, amp)