# Password Storage Bot

Password Storage Bot is a Telegram bot that allows you to securely store and retrieve login/password information for various services. It provides a simple interface for adding, retrieving, and deleting login credentials.

## Getting Started

To use the Password Storage Bot, you need to have a Telegram account. Follow these steps to get started:

1. Create a Telegram account if you don't have one already.
2. Search for the "Password Storage Bot" in the Telegram app or click [here](https://t.me/your_bot_username) to open it directly.
3. Start a conversation with the bot by clicking the "Start" button or sending the "/start" command.
4. The bot will provide you with instructions on how to use it.

## Features

- **Set Password**: Add a new login/password for a service.
- **Get Password**: Retrieve the login/password for a specific service.
- **Delete Password**: Delete the login/password for a service.
- **Show Services**: View the list of services for which you have saved passwords.

## Usage

Once you start a conversation with the bot, you can use the following commands to interact with it:

- `/start`: Start the bot and display the welcome message.
- `/menu`: Display the main menu with available options.
- **SET PASSWORD**: Add a new login/password for a service.
- **GET PASSWORD**: Retrieve the login/password for a specific service.
- **DELETE PASSWORD**: Delete the login/password for a service.
- **SHOW SERVICES**: View the list of services for which you have saved passwords.
- **CANCEL**: Cancel the current operation.

## Deployment

To deploy the Password Storage Bot on your own server or cloud platform, follow these steps:

1. Make sure you have Python 3.9 or later installed on your server or cloud platform.
2. Clone this repository or copy the bot's source code to your server.
3. Install the required dependencies by running the following command:
pip install -r requirements.txt
4. Create a new bot on Telegram by following the instructions in the [Telegram Bot API documentation](https://core.telegram.org/bots#botfather).
5. Obtain the bot token from the BotFather and set it as an environment variable named `BOT_TOKEN` on your server.
6. Run the bot using the following command:
python ftgb.py
7. The bot should now be up and running, ready to accept requests from Telegram users.

## Database

The bot uses an SQLite database to store the login/password information. Each user has their own database file named "passwords_<chat_id>.db" to ensure data privacy.

## Security Considerations

- The bot does not store any sensitive information on its server. All data is stored locally on the user's device.
- It is recommended to use strong and unique passwords for each service you store.
- Be cautious when sharing sensitive information over Telegram, as messages can be intercepted. Avoid storing highly sensitive information in the bot.
- Regularly update your Telegram app to ensure you have the latest security patches.

## Contributing

Contributions to the Password Storage Bot project are welcome! If you encounter any issues or have suggestions for improvement, please open an issue or submit a pull request on the project's GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).


