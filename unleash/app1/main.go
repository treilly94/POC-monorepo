package main

import (
	"flag"
	"net/http"

	"github.com/gin-gonic/gin"

	unleash "github.com/Unleash/unleash-go-sdk/v6"
	unleashcontext "github.com/Unleash/unleash-go-sdk/v6/context"
)

func feature1(ctx unleashcontext.Context) string {
	f1_enabled := unleash.IsEnabled("feature1", unleash.FeatureOptions{Ctx: ctx})
	if f1_enabled {
		return "flag1: enabled"
	} else {
		return "flag1: not enabled"
	}
}

func feature2(ctx unleashcontext.Context) string {
	f2_enabled := unleash.IsEnabled("feature2", unleash.FeatureOptions{Ctx: ctx})
	if f2_enabled {
		return "flag2: enabled"
	} else {
		return "flag2: not enabled"
	}
}

func main() {
	var env = flag.String("e", "development", "environment")
	var port = flag.String("p", "8080", "port")
	flag.Parse()

	var token string

	if *env == "production" {
		println("Running in production mode")
		token = "*:production.aa9059c13a0ea63043c35e14da71dd767be403f6d1b83c152546b6da"
	} else {
		println("Running in development mode")
		token = "default:development.unleash-insecure-api-token"
	}

	err := unleash.Initialize(
		unleash.WithAppName("app1"),
		unleash.WithUrl("http://localhost:4242/api/"),
		unleash.WithProjectName("Default"),
		unleash.WithEnvironment(*env),
		unleash.WithCustomHeaders(http.Header{"Authorization": {token}}),
	)
	if err != nil {
		panic(err)
	}
	defer unleash.Close()

	ctx := unleashcontext.Context{
		UserId:      "user-123",
		SessionId:   "session-abc",
		Environment: *env,
		Properties: map[string]string{
			"plan": "enterprise",
		},
	}

	router := gin.Default()
	router.GET("/f1", func(c *gin.Context) {
		message := feature1(ctx)
		println(ctx.Environment)
		c.JSON(200, gin.H{
			"message": message,
		})
	})
	router.GET("/f2", func(c *gin.Context) {
		ctx.UserId = c.Query("userId")
		println(ctx.UserId)
		message := feature2(ctx)
		c.JSON(200, gin.H{
			"message": message,
		})
	})
	router.Run(":" + *port)
}
