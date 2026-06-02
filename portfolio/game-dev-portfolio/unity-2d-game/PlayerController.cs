using UnityEngine;

/// <summary>
/// 2D 탑다운 RPG 플레이어 움직임 컨트롤러
/// 공고 요건: C# 프로그래밍 기초 + 게임 시스템 개발
/// </summary>
public class PlayerController : MonoBehaviour
{
    [Header("움직임 설정")]
    [SerializeField] private float moveSpeed = 5f;
    
    [Header("스프라이트 참조")]
    [SerializeField] private SpriteRenderer spriteRenderer;
    [SerializeField] private Animator animator;
    
    // 지역 변수
    private Vector2 movement;
    private Rigidbody2D rb;
    private static readonly int IsWalking = Animator.StringToHash("isWalking");
    
    private void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        if (spriteRenderer == null) spriteRenderer = GetComponent<SpriteRenderer>();
        if (animator == null) animator = GetComponent<Animator>();
    }
    
    private void Update()
    {
        HandleInput();
        UpdateAnimation();
    }
    
    private void FixedUpdate()
    {
        Move();
    }
    
    /// <summary>
    /// 플레이어 입력 처리 (WASD / 방향키)
    /// </summary>
    private void HandleInput()
    {
        float horizontal = Input.GetAxisRaw("Horizontal");
        float vertical = Input.GetAxisRaw("Vertical");
        movement = new Vector2(horizontal, vertical).normalized;
    }
    
    /// <summary>
    /// Rigidbody2D를 이용한 물리 기반 이동
    /// </summary>
    private void Move()
    {
        rb.linearVelocity = movement * moveSpeed;
    }
    
    /// <summary>
    /// 애니메이션 업데이트 (방향 전환 + 거리기 상태)
    /// </summary>
    private void UpdateAnimation()
    {
        bool isWalking = movement.magnitude > 0.1f;
        animator.SetBool(IsWalking, isWalking);
        
        if (movement.x < 0)
            spriteRenderer.flipX = true;
        else if (movement.x > 0)
            spriteRenderer.flipX = false;
    }
    
    /// <summary>
    /// 적 괴제당 처리 (Unity Collision System)
    /// </summary>
    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject.CompareTag("Enemy"))
        {
            Debug.Log("적과 충돌! 처리 로직 실행");
            // 처리: 챔 감소, 무적 시간 등
        }
    }
    
    /// <summary>
    /// 아이템 획득 트리거
    /// </summary>
    private void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Item"))
        {
            Debug.Log($"아이템 획득: {other.name}");
            Destroy(other.gameObject);
            // 데이터 백업 등등
        }
    }
}
