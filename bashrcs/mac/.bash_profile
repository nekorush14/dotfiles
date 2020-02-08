if [ -f ~/.bashrc ]; then
  . ~/.bashrc
fi
# bash completion
if [ -f $(brew --prefix)/etc/bash_completion ]; then
  . $(brew --prefix)/etc/bash_completion
fi

# Initializing the rbenv
eval "$(rbenv init -)"

# Setting PATH for Python 3.7
# The original version is saved in .bash_profile.pysave
PATH="/Library/Frameworks/Python.framework/Versions/3.7/bin:${PATH}"
export PATH

HISTSIZE=10000

## PATH for JAVA_HOME

# for open-jdk 8 (AdoptOpenJDK)
export JAVA_HOME=/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/
# for open-jdk 12(AdoptOpenJDK)
# export JAVA_HOME=/Library/Java/JavaVirtualMachines/adoptopenjdk-12.jdk/Contents/Home

# The next line updates PATH for the Google Cloud SDK.
if [ -f '/Users/mitsuhiro/Library/google-cloud-sdk/path.bash.inc' ]; then . '/Users/mitsuhiro/Library/google-cloud-sdk/path.bash.inc'; fi

# The next line enables shell command completion for gcloud.
if [ -f '/Users/mitsuhiro/Library/google-cloud-sdk/completion.bash.inc' ]; then . '/Users/mitsuhiro/Library/google-cloud-sdk/completion.bash.inc'; fi
