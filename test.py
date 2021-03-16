import functools
import hashlib
import inspect
import json
import logging
import os
import re
import subprocess


def run_cmd(cmd, params=None, exc_msg=None):
    """
    Run the given command with the provided parameters.
    :param iter cmd: iterable representing the command to be executed
    :param dict params: keyword parameters for command execution
    :param str exc_msg: an optional exception message when the command fails
    :return: the command output
    :rtype: str
    :raises IIBError: if the command fails
    """
    exc_msg = exc_msg or 'An unexpected error occurred'
    if not params:
        params = {}
    params.setdefault('universal_newlines', True)
    params.setdefault('encoding', 'utf-8')
    params.setdefault('stderr', subprocess.PIPE)
    params.setdefault('stdout', subprocess.PIPE)

    logging.debug('Running the command "%s"', ' '.join(cmd))
    response = subprocess.run(cmd, **params)

    if response.returncode != 0:
        logging.error('The command "%s" failed with: %s', ' '.join(cmd), response.stderr)
        if cmd[0] == 'opm':
            # Capture the error message right before the help display
            regex = r'^(?:Error: )(.+)$'
            # Start from the last log message since the failure occurs near the bottom
            for msg in reversed(response.stderr.splitlines()):
                match = re.match(regex, msg)
                if match:
                   print('iib error')

        print(exc_msg)

    return response.stdout

def skopeo_inspect(*args, return_json=True):
    exc_msg = None
    for arg in args:
        if arg.startswith('docker://'):
            exc_msg = f'Failed to inspect {arg}. Make sure it exists and is accessible to IIB.'
            break
    #skopeo_timeout = get_worker_config().iib_skopeo_timeout
    creds = "1979710|iib:eyJhbGciOiJSUzUxMiJ9.eyJzdWIiOiJhMTIxOGVlMjFjZmY0MTMzOGM0ODQ5MGM5ZmE0OTgwZiJ9.N5d3BYAjnmNA9f0u-2O-8UKU07cJ1mtvakZuu8NO-LYmrSKqpA3LFZpU8zzGH5brcDT2hA-6-_FDQSP5yjPWyI8NNffi3wMLuu7ROyhCzeXW4Zn9V6b8aE6VCpfsRsoKDg94Sn5Z2XkhszN6asxFoe0H0ECxJXUYB60W6cfw2RU5qPbF86HJekztBG4oMeYrRNUbYvrku30GfDwdM4TfAsQcc-4-pQ-Vy8kDlEDmD9FH4L3lPcPX-ii8mLrkdkFvWLMHoCBFF1LkCmEQAjYa2PUv7BK2WzPt8DBvV_4B65q5JyQOhVZVHhiQcDmsBRGpINC4wZkSpeOp3DlgKQpuwYOsm1kggU7KlVNTV_vPN1NusCWl1E6XFKEp0GkLeHt7mi1EgzfEANBYwYdguOuyXRRUayyDC_Mkcbf8XD6zIaZFuS5HlgMO5o2K29Pme2oMftiau2N1PK8RakoKyFzoeSL4uD0Zd2GVIrBT3cJSiv0c1tz8O3P-WmPJj7gduQwuIRdbvaxcVYpIW4bsMG_j1AoStFrOCRr5InFKVAHLxjIwFLQQnErcsv3-aEm7hMDzTfK9NU6TWZm58FJuFBtQJ8s8lIvZtrZBT4tJe1dxEHaYwNCx4QUTpqWYbgI_NVCTHjG_p0BYQ8r9ZpF15VcFuFjDM-5WWT_5EMKZ3753ins"
    cmd = ['skopeo', 'inspect', '--creds', creds] + list(args)
    output = run_cmd(cmd, exc_msg=exc_msg)
    if return_json:
        return json.dumps(output)
    return output

def get_resolved_bundles(bundles):
    
    resolved_bundles = set()
    for bundle_pull_spec in bundles:
        skopeo_raw = skopeo_inspect(f'docker://{bundle_pull_spec}', '--raw')
        if (
            skopeo_raw.get('mediaType')
            == 'application/vnd.docker.distribution.manifest.list.v2+json'
        ):
            # Get the digest of the first item in the manifest list
            digest = skopeo_raw['manifests'][0]['digest']
            #name = _get_container_image_name(bundle_pull_spec)
            #resolved_bundles.add(f'{name}@{digest}')
            print(digest)
        elif (
            skopeo_raw.get('mediaType') == 'application/vnd.docker.distribution.manifest.v2+json'
            and skopeo_raw.get('schemaVersion') == 2
        ):
            print("resolved_bundles.add(get_resolved_image(bundle_pull_spec))")
        else:
            error_msg = (
                f'The pull specification of {bundle_pull_spec} is neither '
                f'a v2 manifest list nor a v2s2 manifest. Type {skopeo_raw.get("mediaType")}'
                f' and schema version {skopeo_raw.get("schemaVersion")} is not supported by IIB.'
            )
            print(error_msg)

    return list(resolved_bundles)
    
def main():
    test = ['docker://registry.stage.redhat.io/ocs4/ocs-operator-bundle:4.6.2-1']
    test2= get_resolved_bundles(test)
    print(test2)

if __name__ == '__main__':
    main()