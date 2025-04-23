#! /bin/python


import subprocess

if import requests, bs4, pandas, lxml, json:
    from bs4 import BeautifulSoup
else:
    subprocess.run(['conda', 'install', '-y', 'requests', 'beautifulsoup4', 'pandas', 'lxml', 'json5'])
    import requests, bs4, pandas, lxml, json
    from bs4 import BeautifulSoup


#adjust maxpackages to your memory supply
maxpackages= 50

#packages to exclude
foundationpackagestoexclude= ['_anaconda_depends', '_libgcc_mutex', '_openmp_mutex']
defectivepackagestoexclude= ['torchvision']

#urls of different package lists
#anaconda relnotes
relnoteurl= "https://www.anaconda.com/docs/getting-started/anaconda/release-notes"
#anaconda main channel linux 64 
mainchannelurllinux64= 'https://repo.anaconda.com/pkgs/main/linux-64/repodata.json'
#anaconda main channel linux arm 64
mainchannelurllinuxarm64= 'https://repo.anaconda.com/pkgs/main/linux-aarch64/repodata.json'
#anaconda main channel linux-s390
mainchannelurlarm64= 'https://repo.anaconda.com/pkgs/main/linux-s390/repodata.json'
#anaconda main channel xosx-arm64
mainchannelurlarm64= 'https://repo.anaconda.com/pkgs/main/xosx-arm64/repodata.json'
#anaconda main channel osx-64
mainchannelurlosx64= 'https://repo.anaconda.com/pkgs/main/linux-aarch64/repodata.json'
#anaconda main channel win-64
mainchannelurlwin64= 'https://repo.anaconda.com/pkgs/main/win-64/repodata.json'


def fetchrelnotepackages(url):
    """
    Fetch package list from relnotepage
    """
    
    try:
        response= requests.get(url)
        response.raise_for_status()
        soup= BeautifulSoup(response.content, 'html.parser')
        
        # Select first table 
        table= soup.find('table')
        if table:
            df= pd.read_html(str(table))[0]
            package_names= df.iloc[:, 0].tolist()
            return package_names
        else:
            print("No table found on the page.")
            return []
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return []
    except pd.errors.EmptyDataError:
        print("No data found in the table.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def fetchchannelpackages(url):
    """
    Fetch channel package list
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
    
    # reduce to unique
    packages= list(set(packages))
    
    if not packages:
        print("No packages found")
    else:
        print(f"Found {len(packages)} packages")
    
    return packages


def installpackages(packages, maxpackages=maxpackages):
    """
    Install packages
    """
    
    packages= list( set(packages) -set(foundationpackagestoexclude) -set(defectivepackagestoexclude))
    packages= packages[0:maxpackages]
    
    
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
    
    packages= fetchrelnotepackages(relnoteurl)
    # packages= fetchchannelpackages(mainchannelurllinux64)
    # packages= fetchchannelpackages(mainchannelurllinuxarm64)
    
    print("")
    print("list of packages fetched")
    print(packages)
    print("")
    
    installpackages(packages=packages)


