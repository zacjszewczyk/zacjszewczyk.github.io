Function pull {
    git subtree pull --prefix=html git@github.com:zacjszewczyk/zacjszewczyk.github.io.git master
    git pull origin master
}

Function deploy {
    git add -A
    git commit -m "Deployment commit on $(date)"
    git subtree push --prefix=html git@github.com:zacjszewczyk/zacjszewczyk.github.io.git master
    git push origin master
}

if ($args.count -gt 0) {
    if ($args[0] -eq "pull") {
        pull
    } elseif ($args[0] -eq "deploy") {
        deploy
    } else {
        Write-Warning -Message "Invalid parameter. Please try again."
    }
} else {
    Write-Output @"
Supported Commands

pull`t`tPull from my GitHub
deploy`t`tPush to remote repos
"@
}