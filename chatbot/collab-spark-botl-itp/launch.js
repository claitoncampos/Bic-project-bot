{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "WebexTeamsBot",
            "type": "python",
            "request": "launch",
            "stopOnEntry": false,
            "pythonPath": "${config:python.pythonPath}",
            "program": "${workspaceRoot}/run_bot.py",
            "cwd": "${workspaceRoot}",
            "debugOptions": [
                "WaitOnAbnormalExit",
                "WaitOnNormalExit",
                "RedirectOutput"
            ],
            "args": [],
            "env": {
                "TEAMS_ACCESS_TOKEN": "ZjZlM2YzMzctZmQ3ZC00OWRhLTgzODItMzIzODI3NTM3ZDY1NDllZTI1ZDItM2Ew_PF84_9f031aba-6be6-431f-9917-cb1f996f5b45"
            }
        }
    ]
}