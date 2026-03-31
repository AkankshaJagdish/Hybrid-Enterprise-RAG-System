using System.Net.Http.Json;

public class PythonService
{
    private readonly HttpClient _httpClient;

    public PythonService(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<object?> QueryAsync(QueryRequest request)
    {
        var response = await _httpClient.PostAsJsonAsync(
            "/query", request);

        response.EnsureSuccessStatusCode();

        return await response.Content.ReadFromJsonAsync<object>();
    }

    public async Task<string> UploadDocumentAsync(IFormFile file)
    {
        using var content = new MultipartFormDataContent();

        var fileContent = new StreamContent(file.OpenReadStream());
        content.Add(fileContent, "file", file.FileName);

        var response = await _httpClient.PostAsync("/upload", content);

        response.EnsureSuccessStatusCode();

        return await response.Content.ReadAsStringAsync();
    }
}