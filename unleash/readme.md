# Unleash

a poc for the (unleash)[https://docs.getunleash.io/] feature flag tool

Theres a compose file that starts a local unleash instance and a small go app
that implements the sdk to enable and disable features

There are also bruno commands to hit the api for the app

```
# dev app
go run .

# prod app
go run . -e production -p 8081
```
