from os import walk, path
from prefect import Client
from importlib import import_module
from itertools import groupby

client = Client()
flows = client.graphql('''query {
    flow { project { name } archived name id }
}''').to_dict()['data']['flow']

flows_by_project = {
    project: { flow['id']: flow['name'] for
        flow in filter(lambda flow: not flow['archived'], project_flows) 
    }
    for project, project_flows in groupby(flows, lambda flow: flow['project']['name'])
}

(root, projects, _) = next(walk(path.dirname(__file__)))

for project_name in projects:
    if project_name in flows_by_project:
        for old_flow in flows_by_project[project_name].keys():
            error = client.graphql(f'''mutation {{
                archive_flow(input: {{ flow_id: "{old_flow}" }}) {{ error }}
            }}''').to_dict()['data']['archive_flow']['error']

            print('Archiving existing flow %s.. %s' % (old_flow, error or 'OK'))

    files = next(walk(path.join(root, project_name)))[-1]

    for file in files:
        if not file.endswith('.py'): continue
        module = path.splitext(file)[0]
        
        flow = getattr(import_module('.%s.%s' % (project_name, module), __name__), 'flow')
        if callable(getattr(flow, 'register', None)):
            if (project_name not in flows_by_project) and file == files[0]:
                client.create_project(project_name)
 
            flow.register(project_name)
            flow.visualize(
                format='png',
                filename=path.join(root, project_name, module))

