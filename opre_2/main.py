class Task:
    def __init__(self, name):
        self.name = name
        self.commands = []
        self.waiting_for = None
        self.time = 1

    def __repr__(self):
        return f"Task({self.name},{[self.commands]},{self.waiting_for.name if self.waiting_for is not None else 'Semmi'}, {self.time})"


class Resource:
    def __init__(self, name):
        self.name = name
        self.this_task_use_me = None
        self.waiting_for = []

    def __repr__(self):
        return f"Resource({self.name},{[n.name for n in self.waiting_for]},{self.this_task_use_me})"

    def remove(self):
        if self.this_task_use_me is not None:
            self.this_task_use_me.waiting_for.remove(self)
            self.this_task_use_me = None

        for task in self.waiting_for:
            task.waiting_for.remove(self)

        self.waiting_for.clear()


tasks = []
resources = set()

while True:
    try:
        input_str = input().strip()
        input_list = input_str.split(',')

        task_name = input_list[0]
        task_inputs = [x.strip() for x in input_list[1:]]

        task = Task(task_name)
        task.commands = task_inputs

        tasks.append(task)

        for command in task.commands:
            if command.startswith('+') or command.startswith('-'):
                resources.add(command[1:])

    except EOFError:
        break

resource_objects = [Resource(resource) for resource in resources]
out = []



def check_deadlocks():
    for resource in resource_objects:
        if resource.this_task_use_me is not None:
            visited = set()

            def dfs(task):
                if task in visited:
                    return True
                visited.add(task)

                if task.waiting_for is not None:
                    if task.waiting_for.this_task_use_me is not None and dfs(task.waiting_for.this_task_use_me):
                        return True

                visited.remove(task)

                return False

            if dfs(resource.this_task_use_me):
                return resource.this_task_use_me, resource.name

    return None


while any(task.commands for task in tasks):
    for task in tasks:
        #print(task)
        #print(resource_objects)

        if task.commands:
            command = task.commands.pop(0)

            if command.startswith("+"):
                resource_name = command[1:]
                resource = next(res for res in resource_objects if res.name == resource_name)

                if resource.this_task_use_me is None:
                    resource.this_task_use_me = task
                else:
                    task.waiting_for = resource
                    resource.waiting_for.append(task)
                    #deadlock
                    deadlock = check_deadlocks()

                    if deadlock is not None:
                        out.append((task.name, task.time, resource.name))
                        task.waiting_for = None
                        #print(out)

            elif command.startswith("-"):
                resource_name = command[1:]
                resource = next(res for res in resource_objects if res.name == resource_name)

                if resource.this_task_use_me == task:
                    if not resource.waiting_for:
                        resource.this_task_use_me = None
                    else:
                        resource.this_task_use_me = resource.waiting_for.pop(0)
                        resource.this_task_use_me.waiting_for = None

        #print(task)
        #print(resource_objects)
        #print()
        task.time += 1


for ki in out:
    print(str(ki[0]) + ',' + str(ki[1]) + ',' + str(ki[2]))

