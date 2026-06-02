using UnityEngine;

/// <summary>
/// 간단한 적 AI (추적 + 공격)
/// 공고 요건: 게임 콘텐츠 밌 시스템 개발
/// </summary>
public class EnemyController : MonoBehaviour
{
    [Header("적 설정")]
    [SerializeField] private float moveSpeed = 3f;
    [SerializeField] private int attackDamage = 10;
    [SerializeField] private float attackRange = 1.5f;
    [SerializeField] private float detectionRange = 8f;
    
    private Transform player;
    private Rigidbody2D rb;
    private bool isChasing = false;
    
    private void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        player = GameObject.FindGameObjectWithTag("Player")?.transform;
    }
    
    private void Update()
    {
        if (player == null || GameManager.Instance?.isGameOver == true)
        {
            rb.linearVelocity = Vector2.zero;
            return;
        }
        
        float distanceToPlayer = Vector2.Distance(transform.position, player.position);
        
        if (distanceToPlayer <= detectionRange)
        {
            if (distanceToPlayer > attackRange)
                ChasePlayer();
            else
                AttackPlayer();
        }
        else
        {
            Idle();
        }
    }
    
    /// <summary>
    /// 플레이어 추적
    /// </summary>
    private void ChasePlayer()
    {
        isChasing = true;
        Vector2 direction = (player.position - transform.position).normalized;
        rb.linearVelocity = direction * moveSpeed;
        
        // 스프라이트 방향 전환
        GetComponent<SpriteRenderer>().flipX = direction.x < 0;
    }
    
    /// <summary>
    /// 플레이어 공격
    /// </summary>
    private void AttackPlayer()
    {
        rb.linearVelocity = Vector2.zero;
        
        // 공격 코루틴 (실제로는 공격 애니메이션 트리거)
        // 여기서는 방어로 달려들어 줌처리
        GameManager.Instance?.TakeDamage(attackDamage);
    }
    
    /// <summary>
    /// 대기 상태
    /// </summary>
    private void Idle()
    {
        isChasing = false;
        rb.linearVelocity = Vector2.zero;
    }
    
    /// <summary>
    /// 적 공격 범위 시각화 (Scene 뷰에만)
    /// </summary>
    private void OnDrawGizmosSelected()
    {
        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(transform.position, attackRange);
        
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireSphere(transform.position, detectionRange);
    }
}
