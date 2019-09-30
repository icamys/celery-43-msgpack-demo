import logging

from celery import shared_task, chain, group, Celery, Task

app = Celery('tasks', broker='pyamqp://guest@localhost//')


class CreateListTask(Task):
    name_plain = 'create_list'
    namespace = 'ns'

    @property
    def name(self):
        return self.namespace + ':' + self.name_plain

    def run(self, *args, **kwargs):
        return ['google.com']


class ProcessOneTask(Task):
    name_plain = 'process_one'
    namespace = 'ns'

    @property
    def name(self):
        return self.namespace + ':' + self.name_plain

    def run(self, the_list, number):
        logging.info(str(the_list) + ' ' + str(number + 1))
        return the_list


class ProcessTwoTask(Task):
    name_plain = 'process_two'
    namespace = 'ns'

    @property
    def name(self):
        return self.namespace + ':' + self.name_plain

    def run(self, the_list, number):
        logging.info(str(the_list) + ' ' + str(number + 2))
        return the_list


app.tasks.register(CreateListTask())
app.tasks.register(ProcessOneTask())
app.tasks.register(ProcessTwoTask())

res = chain(
    CreateListTask().s(),
    group([ProcessOneTask().s(i) | ProcessTwoTask().s(i) for i in range(2)])
)()
