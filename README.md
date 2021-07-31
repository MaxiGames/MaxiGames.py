# MaxiGames

Your one and only discord bot that includes all forms of mini games you will ever want. Have a suggestion for another? Open an issue! :D

## Future Implementations

### Commands

- tictactoe (implemented)
- typeracer
- blackjack 
- chess? wow so hard
- uno?????
- pictionary!
- that telephone game?
- google snake game with button
- let me google that for you (implemented)
- guess the song
- random guessing (well kind of :D)

### Troubleshooting tips

#### Discord SSL certificate validation error

If you get errors like the following when running, it's due to outdated certificate root. 
```
raise ClientConnectorCertificateError(req.connection_key, exc) from exc
aiohttp.client_exceptions.ClientConnectorCertificateError: Cannot connect to host discord.com:443 ssl:True [SSLCertVerificationError: (1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1129)')]
```

Referring to this POST: https://stackoverflow.com/questions/62202252/ssl-1108-mac-issue, you can resolve the issue by running the `Install Certificates.command` under `Applications/Python 3.x` folder 