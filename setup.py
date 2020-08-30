from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
curVersion = '10.6'
buildOptions = dict(excludes = ["_bz2", "_codecs", "_codecs_cn", "_codecs_hk", "_codecs_iso2022", "_codecs_jp", "_codecs_kr", "_codecs_tw"], packages = ["textToTable", "txt_to_XLgraphs", "checkText", "definedExceptions"]) 
buildOptions['build_exe'] = 'source/txt_to_XLgraphs_linux64_v' + curVersion
buildOptions['include_files'] = [("license/velosph_sm_cmx.png", "license/velosph_sm_cmx.png"), "README.txt"] 
buildOptions['include_files'].append("structure_patterns.txt")
buildOptions['include_files'].append("About.txt")
buildOptions['include_files'].append(("license/license.txt", "license/license.txt"))
buildOptions['include_files'].append(("examples/test_format.txt", "examples/test_format.txt"))
buildOptions['include_files'].append(("examples/test_csv.csv", "examples/test_csv.csv"))
buildOptions['include_files'].append('txt_to_XLgraphs_start.sh')
buildOptions['icon'] = "cup.ico"
buildOptions['include_files'].append("cup.ico")
buildOptions['optimize'] = 2

import sys
base = 'Console' 
#if sys.platform=='win32':
#    base = "Win32GUI"

executables = [
    Executable('txt_to_XLgraphs.py', base=base, targetName = 'txt_to_XLgraphs', icon = 'cup.ico')
]

setup(name='txt_to_XLgraphs',
      version = curVersion,
      description = 'Converts text like statistics to graphics compatible with office programms.',
      author = 'Evgeny Lobov',
      author_email = 'ewhenel@gmail.com',
      options = dict(build_exe = buildOptions),
      executables = executables)
