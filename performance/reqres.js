import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metric to track request error rate
const errorRate = new Rate('api_errors');

const BASE_URL = __ENV.REQRES_BASE_URL || 'https://reqres.in';
const API_KEY = __ENV.REQRES_API_KEY || '';

export const options = {
  vus: 10,
  duration: '30s',
  thresholds: {
    // Quality criteria defined for this technical assessment (not official ReqRes SLAs)
    http_req_failed: ['rate<0.01'], // Error rate under 1%
    http_req_duration: ['p(95)<1000'], // 95% of requests should respond in less than 1000ms
    checks: ['rate>0.99'], // 99%+ of functional assertions must pass
  },
};

export default function () {
  const headers = {
    'Accept': 'application/json',
    'User-Agent': 'k6-performance-assessment/1.0',
  };

  if (API_KEY) {
    headers['x-api-key'] = API_KEY;
  }

  // Flow 1: Retrieve paginated list of users (GET /api/users?page=2)
  {
    const res = http.get(`${BASE_URL}/api/users?page=2`, { headers });
    const success = check(res, {
      'status is 200': (r) => r.status === 200,
      'has users page 2': (r) => {
        try {
          const body = JSON.parse(r.body);
          return body.page === 2 && Array.isArray(body.data) && body.data.length > 0;
        } catch (_) {
          return false;
        }
      },
    });
    errorRate.add(!success);
  }

  sleep(0.5); // Controlled pacing to prevent aggressive rate limiting against public API

  // Flow 2: Retrieve specific user details (GET /api/users/2)
  {
    const res = http.get(`${BASE_URL}/api/users/2`, { headers });
    const success = check(res, {
      'status is 200': (r) => r.status === 200,
      'has valid user id 2': (r) => {
        try {
          const body = JSON.parse(r.body);
          return body.data && body.data.id === 2;
        } catch (_) {
          return false;
        }
      },
    });
    errorRate.add(!success);
  }

  sleep(1); // Think time between iterations
}
