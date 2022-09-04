eval "$(/opt/homebrew/bin/brew shellenv)"

# bash completion
if [ -f $(brew --prefix)/etc/bash_completion ]; then
  . $(brew --prefix)/etc/bash_completion
fi

# Initializing the rbenv
if which rbenv > /dev/null; then eval "$(rbenv init -)"; fi

# Setting PATH for Python 3.7
# The original version is saved in .bash_profile.pysave
PATH="/Library/Frameworks/Python.framework/Versions/3.7/bin:${PATH}"
export PATH

HISTSIZE=10000

## PATH for JAVA_HOME

# for open-jdk 11 (AdoptOpenJDK)
export JAVA_HOME=/Library/Java/JavaVirtualMachines/temurin-11.jdk/Contents/Home/
# for open-jdk 12(AdoptOpenJDK)
# export JAVA_HOME=/Library/Java/JavaVirtualMachines/adoptopenjdk-12.jdk/Contents/Home

# The next line updates PATH for the Google Cloud SDK.
if [ -f '/Users/mitsuhiro/Library/google-cloud-sdk/path.bash.inc' ]; then . '/Users/mitsuhiro/Library/google-cloud-sdk/path.bash.inc'; fi

# The next line enables shell command completion for gcloud.
if [ -f '/Users/mitsuhiro/Library/google-cloud-sdk/completion.bash.inc' ]; then . '/Users/mitsuhiro/Library/google-cloud-sdk/completion.bash.inc'; fi

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/Users/l12s/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
  eval "$__conda_setup"
else
  if [ -f "/Users/l12s/miniconda3/etc/profile.d/conda.sh" ]; then
    . "/Users/l12s/miniconda3/etc/profile.d/conda.sh"
  else
    export PATH="/Users/l12s/miniconda3/bin:$PATH"
  fi
fi
unset __conda_setup
# <<< conda initialize <<<

export BASH_SILENCE_DEPRECATION_WARNING=1
# eval "$(oh-my-posh init bash --config /opt/homebrew/opt/oh-my-posh/themes/iterm2.omp.json)"

if [ -f ~/.bashrc ]; then
  . ~/.bashrc
fi
