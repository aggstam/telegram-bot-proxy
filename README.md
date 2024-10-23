# telegram-bot-proxy
`Telegram` bots become better and better by the day, providing extremely useful information thats handy to have accessible
by just a simple command prompt. BUT most(if not all) of them are closed source, hosted in a centralized service,
constantly sniffing all your group messages until a prompt arrives. How can you be sure that the bot reads just the
messages its supposed to and nothing more? This is a great opsec vulnerability, and unless bots providers open source
their code and provide self hosting capabilities, you should *never* use such services.

Alas anon, there is a solution, more like a ducktaping, to this issue. This repo provides a self hosting
proxy, which you can configure to retrieve specific prompt messages and forward them to a fully restricted group,
which will contain the sus bot, similar to how you would firejail a program to not access parts of your system
while its running. That way you can rest assure, the bot only reads command prompt messages and nothing else,
giving you the juicy alpha you so desire.

Since telegram bots can't read each others messages, you are required to create an API ID and HASH for your(or a random)
account, to use with this setup, following the official docs: https://core.telegram.org/api/obtaining_api_id#obtaining-api-id
To setup the proxy, you also need to create a new group, that will contain the sus bots, and grab both that group and your
main group IDs, to use in the configuration. Your user must exist in both groups so your proxy can "forward" the messages
bettween them. The proxy only forwards messages using the prompt prefix `/p`.

After you obtained your key, you can configure the proxy by simply editting the Makefile with your config options:
| Config         | Description                                                            |
|----------------|------------------------------------------------------------------------|
| `API_ID`       | Your API key, provided by `telegram`                                   |
| `API_HASH`     | Your API hash, provided by `telegram`                                  |
| `PHONE`        | Your `telegram` account phone number                                   |
| `DB_PASS`      | Password used to encrypt the account information                       |
| `GROUP_ID`     | The `tg` group you want to protect from sniffers                       |
| `BOTS_GROUP_ID`| The `tg` group you want to dump all the trash bots and protect against |

## Usage
Script provides the following Make targets:
| Target      | Description                             |
|-------------|-----------------------------------------|
| `bootstrap` | Create the environment and get all deps |
| `clean`     | Remove build artifacts                  |
| `deploy`    | Start the proxy using the configuration |

### Environment setup
The following OS dependencies are required:
|   Dependency   |
|----------------|
| git            |
| make           |
| python         |
| python-venv    |
| libssl1.1      |

Before first usage, you have to grab all the required python libraries:
```
% make bootstrap
```
### Execution
Since we are using a `python` virtual environment, we have to source
it before starting the proxy:
```
% . {FULL_PATH_REPO}/venv/bin/activate
```
After that, you can modify the configuration and start the proxy:
```
% make deploy
```
After the proxy is up and running, you can verify it's working by
sending a prompt using the `/p` prefix, like `/p /c btc`.
You should see your account posting the message `/c btc` in the bots jail group
and after the bot respond the message should be forwarded back to your main group.
