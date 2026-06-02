using UnityEngine;
using UnityEngine.SceneManagement;

/// <summary>
/// 게임 전역 발들임 (Singleton Pattern)
/// 공고 요건: 게임 콘텐츠 유지보수 및 라이브서비스 운영
/// </summary>
public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }
    
    [Header("게임 스테이트")]
    public int score = 0;
    public int playerHealth = 100;
    public int currentStage = 1;
    public bool isGameOver = false;
    
    [Header("서비스 연동")]
    [SerializeField] private string apiBaseUrl = "http://localhost:5000";
    
    private void Awake()
    {
        // 싱글턴 패턴: 쌌다를 허용하지 않음
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }
        Instance = this;
        DontDestroyOnLoad(gameObject); // 쌌 시 유지
        
        LoadGameData();
    }
    
    /// <summary>
    /// 점수 추가
    /// </summary>
    public void AddScore(int points)
    {
        score += points;
        Debug.Log($"현재 점수: {score}");
        
        // 서버에 점수 전송 (비동기)
        StartCoroutine(SendScoreToServer(score));
    }
    
    /// <summary>
    /// 플레이어 데미지 처리
    /// </summary>
    public void TakeDamage(int damage)
    {
        if (isGameOver) return;
        
        playerHealth -= damage;
        if (playerHealth <= 0)
        {
            playerHealth = 0;
            GameOver();
        }
    }
    
    /// <summary>
    /// 게임 오버 처리
    /// </summary>
    private void GameOver()
    {
        isGameOver = true;
        Debug.Log("Game Over! 최종 점수: " + score);
        
        // 서버에 최종 점수 저장
        StartCoroutine(SendFinalScore(score));
        
        // 오버 UI 표시 (실제로는 UIManager를 호출)
        // UIManager.Instance.ShowGameOver(score);
    }
    
    /// <summary>
    /// 스테이지 이동
    /// </summary>
    public void NextStage()
    {
        currentStage++;
        SaveGameData();
        SceneManager.LoadScene($"Stage{currentStage}");
    }
    
    /// <summary>
    /// 데이터 저장 (PlayerPrefs 기반)
    /// </summary>
    private void SaveGameData()
    {
        PlayerPrefs.SetInt("Score", score);
        PlayerPrefs.SetInt("Health", playerHealth);
        PlayerPrefs.SetInt("Stage", currentStage);
        PlayerPrefs.Save();
    }
    
    /// <summary>
    /// 데이터 로드
    /// </summary>
    private void LoadGameData()
    {
        score = PlayerPrefs.GetInt("Score", 0);
        playerHealth = PlayerPrefs.GetInt("Health", 100);
        currentStage = PlayerPrefs.GetInt("Stage", 1);
    }
    
    /// <summary>
    /// 서버에 점수 전송 (비동기 HTTP 통신)
    /// 공고 요건: 게임 개발에 필요한 각종 서비스 시스템
    /// </summary>
    private System.Collections.IEnumerator SendScoreToServer(int currentScore)
    {
        string json = $"{{\"score\":{currentScore}, \"stage\":{currentStage}}}";
        byte[] body = new System.Text.UTF8Encoding().GetBytes(json);
        
        using (UnityEngine.Networking.UnityWebRequest request = new UnityEngine.Networking.UnityWebRequest(
            $"{apiBaseUrl}/api/score", "POST"))
        {
            request.uploadHandler = new UnityEngine.Networking.UploadHandlerRaw(body);
            request.downloadHandler = new UnityEngine.Networking.DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");
            
            yield return request.SendWebRequest();
            
            if (request.result == UnityEngine.Networking.UnityWebRequest.Result.Success)
                Debug.Log("서버 저장 성공!");
            else
                Debug.LogWarning($"서버 저장 실패: {request.error}");
        }
    }
    
    private System.Collections.IEnumerator SendFinalScore(int finalScore)
    {
        yield return SendScoreToServer(finalScore);
    }
    
    /// <summary>
    /// 게임 초기화
    /// </summary>
    public void RestartGame()
    {
        score = 0;
        playerHealth = 100;
        currentStage = 1;
        isGameOver = false;
        SaveGameData();
        SceneManager.LoadScene("MainScene");
    }
}
