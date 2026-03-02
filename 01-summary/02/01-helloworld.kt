import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject

class QwenClient(private val apiKey: String, private val baseUrl: String) {

    private val client = OkHttpClient()
    private val jsonMediaType = "application/json; charset=utf-8".toMediaType()

    fun chatCompletion(
        model: String,
        messages: List<Map<String, String>>,
        enableThinking: Boolean = false,
        enableSearch: Boolean = false
    ) {
        val requestBody = JSONObject().apply {
            put("model", model)
            put("messages", messages.map { JSONObject(it) })
            put("stream", true)
            put("extra_body", JSONObject().apply {
                put("enable_thinking", enableThinking)
                put("enable_search", enableSearch)
            })
        }

        val request = Request.Builder()
            .url("$baseUrl/chat/completions")
            .post(requestBody.toString().toRequestBody(jsonMediaType))
            .addHeader("Authorization", "Bearer $apiKey")
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: java.io.IOException) {
                println("请求失败：${e.message}")
            }

            override fun onResponse(call: Call, response: Response) {
                response.body?.string()?.let { responseBody ->
                    println(responseBody)
                }
            }
        })
    }
}

fun main() {
    println("Hello, World!")
    // model: qwen3.5-plus
    // api_key: sk-cc52517c86af46229520c677a78a1739

    val client = QwenClient(
        apiKey = "sk-ea696c7fcc5a44efb003c7876cb02bc1",
        baseUrl = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    val messages = listOf(mapOf("role" to "user", "content" to "今天南京的天气？"))

    println("\n" + "=".repeat(20) + "思考过程" + "=".repeat(20))

    // 注意：Kotlin 版本使用了简化的流式处理，如需完整流式解析，需要进一步处理 SSE 格式
    client.chatCompletion(
        model = "qwen3.5-flash-2026-02-23",
        messages = messages,
        enableThinking = false,
        enableSearch = true
    )

    // 给异步请求一些时间完成
    Thread.sleep(5000)
}
