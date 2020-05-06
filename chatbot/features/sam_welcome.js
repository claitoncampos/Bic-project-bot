//
// Interação inicial do bot com o usuário
//

const { BotkitConversation} = require( 'botkit' );

module.exports = function ( controller ) {

    const convo = new BotkitConversation( 'sam_welcome', controller);

    convo.say( 'Ola, eu sou o S.A.M, seu assistente pessoal');
    convo.say( 'Você pode a qualquer momento solicitar informações\n' +
        'sobre sua loja, para isso basta você escrever (loja)\n' +
        'e lhe apresentarei algumas possibilidades de interação' );

    controller.addDialog( convo );

    controller.hears( 'sam', 'message, direct_message', async (bot, message) => {

        await bot.beginDialog( 'sam_welcome' );
    });

    controller.commandHelp.push( { command: 'sam', text: 'Info about the store (Botkit conversations'})
};