#! /bin/python3


import subprocess


subprocess.run(['conda', 'install', '-y', 'python', 'json5', 'requests'])


import json
import requests
# import urllib.request


#anacondarepo 64amd 
anacurl= 'https://repo.anaconda.com/pkgs/main/linux-64/repodata.json'

#anacondarepo 64aarch
# anacurl= 'https://repo.anaconda.com/pkgs/main/linux-aarch64/repodata.json'

# anaconda distribution package list and miniconda distribution package list are not publicly availabe


def fetchpackages(url):
    """
    Fetch the package list
    """
    
    try:
        with requests.get(url) as response:
            pkgdata= json.loads(response.text)
    
    except requests.error.GETError as e:
        print(f"Error on fetch data from {repo_url}: {e}")
        return
            
    except json.JSONDecodeError as e:
        print(f"Error on decode JSON from {repo_url}: {e}")
        return
    
    pkgkeys= list(pkgdata['packages'].keys())
    
    packages= []
    for i in range(0, len(pks)):
            name= pkgkeys[i].split("-")[0]
            version= pkgkeys[i].split("-")[1]
            # package_spec= name +"-" +version
            package_spec= name    
            packages.append(package_spec)
    
    # reduce to unique; no stable sort
    packages= list(set(packages))
    
    if not packages:
        print("No packages found")
    else:
        print(f"Found {len(packages)} packages")
    
    return packages


def installpackages(packages, maxpackages=100):
    """
    Install packages
    """

    packages= packages[:maxpackages]
    
    print(f"Going to install {len(packages)} packages")
       
    for i in range(0, len(packages)):   
        # name= packages[i].split("-")[0]
        # version= packages[i].split("-")[1]
        name= packages[i]
               
        # if name and version:
        if name:
            # package_spec = f"{name}=={version}"
            package_spec = f"{name}"
            print(f"Try to install {package_spec}...")
            try:
                subprocess.run(['conda', 'install', '-y', package_spec], check=True)
                print(f"Successfully installed {package_spec}")
            except subprocess.CalledProcessError as e:
                print(f"Error on install of {package_spec}: {e}")
        else:
            print(f"Skip package {name} because of missing name or version")
    
    print("Package installation process complete")


if __name__ == "__main__":
    packages= fetchpackages(anacurl)
    installpackages(packages=packages)


