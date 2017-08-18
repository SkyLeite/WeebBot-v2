var passport = require('passport');
var session = require('express-session');
var fetch = require('node-fetch');
var OAuth2Strategy = require('passport-oauth2').Strategy;
var db = require('sqlite');

module.exports = (app) => {

    app.use(session({
        secret: 'asdfasdfasdf',
        resave: true,
        saveUninitialized: true,
        cookie: { secure: false, maxAge: (4 * 60 * 60 * 1000) },
    }));

    app.use(passport.initialize());
    app.use(passport.session());

    passport.use(new OAuth2Strategy({
        authorizationURL: 'https://discordapp.com/api/oauth2/authorize',
        tokenURL: 'https://discordapp.com/api/oauth2/token',
        clientID: '347766221111951377',
        clientSecret: '5KDmQJA1qMt9uhpZpVRHATmhXBegRdnK',
        callbackURL: "/auth/discord/callback",
        scope: ['guilds', 'identify']
    },
        async function (accessToken, refreshToken, profile, cb) {
            let user = await (await fetch('https://discordapp.com/api/users/@me', {
                method: 'GET',
                headers: { Authorization: 'Bearer ' + accessToken }
            })).json();

            let guilds = await (await fetch('https://discordapp.com/api/users/@me/guilds', {
                method: 'GET',
                headers: { Authorization: 'Bearer ' + accessToken }
            })).json();

            return cb(null, { user, guilds, accessToken });
        }
    ));

    passport.serializeUser(function (user, done) {
        done(null, user);
    });

    passport.deserializeUser(function (user, done) {
        done(null, user);
    });

    app.get('/auth/discord', passport.authenticate('oauth2'));

    app.get('/auth/discord/callback',
        passport.authenticate('oauth2', { failureRedirect: '/login' }), (req, res) => {
            res.redirect('/');
        });

    app.get('/api', async (req, res) => {
        res.send({ version: '1.0.0' });
    });

    app.get('/api/logout', async (req, res) => {
        req.logout();
        res.redirect('/');
    })

    app.get('/api/me', async (req, res) => {
        if (!req.isAuthenticated()) res.status(401).send({ STATUS_CODE: 401 });
        res.send(req.user);
    });

    app.get('/api/guild/:id/channels', async (req, res) => {
        if (!req.isAuthenticated()) res.status(401).send({ STATUS_CODE: 401 });

        let channels = await (await fetch('https://discordapp.com/api/guilds/' + req.query.id + '/channels', {
            method: 'GET',
            headers: { Authorization: 'Bearer ' + req.user.accessToken }
        })).json();
        res.send(channels)
    });

    app.get('/api/settings', async (req, res) => {
        if (!req.isAuthenticated()) res.redirect('/auth/discord');
        try {
            await db.open(__dirname.replace(/admin\\server\\middlewares/, '') + 'settings.sqlite3');
            let result = [];

            for (let i of (await db.all("SELECT * FROM settings"))) {
                result.push({ guild: i.guild, settings: JSON.parse(i.settings) });
            }
            res.send(result);
        } catch (err) {
            res.status(500).send(err);
        }
    });
}