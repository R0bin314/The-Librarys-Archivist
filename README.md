# **The Library's Archivist**
The Library's Archivist is a moderation and archival bot used by the [The Library](https://discord.com/invite/FMzRtuy), a book piracy server. Its primary function is to automatically index, catalogue, and archive the contents of The Library, as well as provide information about its contents. It also has the ability to ban and kick users.

## How The Library's Archivist Works
The bot itself was written in Python, using [Discord.py](https://github.com/Rapptz/discord.py).
The archiving process, however, is a *tad* more complicated.

**Here's how it works:**
1. The bot archives the entire server into CSV files using [DiscordChatExporter.cli](https://github.com/Tyrrrz/DiscordChatExporter)
2. It deletes all of the chat channels, leaving only channels which contains books.
3. It parses the CSV files, only leaving the message content.
4. It parses the message contents, and seperates them into a title and author using `csv_parse()`
5. This information is added to an SQLite database using [SQLite3](https://docs.python.org/3/library/sqlite3.html)
