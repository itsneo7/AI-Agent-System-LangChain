conda-forge Instead 

If you prefer to avoid Anaconda's commercial repository channels and use the community-maintained conda-forge channel instead, you can configure Conda to bypass defaults:

Block defaults Globally (Recommended)

Run these two commands to remove the base Miniconda .condarc file and tell Conda never to fall back to defaults:

Remove-Item C:\Users\yuvisij\miniconda3\.condarc
conda config --add channels nodefaults
conda config --show channels

Verify that defaults is completely gone (it should show only conda-forge and nodefaults)

Then create your environment:
conda create -n langchain python=3.11 -y
conda init
conda activate langagent
pip install -r req.txt


