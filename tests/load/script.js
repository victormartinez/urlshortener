import http from "k6/http";
import { check } from "k6";

export function setup() {
    const data = { "destination_url": "https://google.com" }
    const headers = { "Content-Type": "application/json" }
    const res = http.post("http://localhost:8080/",
        JSON.stringify(data),
        { headers: headers }
    );
    const body = res.json()
    console.log("CODE:", body["code"])
    return { data: body };
}

export const options = {
    scenarios: {
        warm_up: {
            executor: "constant-vus",
            duration: "5s",
            startTime: "0s",
            vus: 1,
        },
        rump_up_load: {
            executor: "ramping-vus",
            startVUs: 1,
            startTime: "5s",
            stages: [
                { duration: "20s", target: 500 },
            ],
        },
        constant_request_rate: {
            executor: 'constant-arrival-rate',
            startTime: "25s",
            rate: 10000,
            timeUnit: '1m',
            duration: '1m',
            preAllocatedVUs: 500,
            maxVUs: 1000,
        },
    },
    thresholds: {
        "http_req_duration{status:200}": ["max>=0"],
        "http_req_duration{status:201}": ["max>=0"],
        "http_req_duration{status:202}": ["max>=0"],
        "http_req_duration{status:307}": ["max>=0"],
        "http_req_duration{status:308}": ["max>=0"],
        "http_req_duration{status:400}": ["max>=0"],
        "http_req_duration{status:401}": ["max>=0"],
        "http_req_duration{status:403}": ["max>=0"],
        "http_req_duration{status:404}": ["max>=0"],
        "http_req_duration{status:409}": ["max>=0"],
        "http_req_duration{status:500}": ["max>=0"],
        "http_req_duration{status:501}": ["max>=0"],
        "http_req_duration{status:502}": ["max>=0"],
        "http_req_duration{status:503}": ["max>=0"],
        "http_req_duration{status:504}": ["max>=0"]
    },
    summaryTrendStats: ["avg", "min", "max", "p(90)", "p(95)", "count"],
    tags: {
        executed_at: new Date().toJSON(),
    },
};

export default function (data) {
    const code = data.data["code"];
    const url = `http://localhost:8080/${code}?redirect=False`;
    const res = http.get(url);
    const validStatus = [200, 201, 307];
    check(res, {
        'is status success': (r) => validStatus.includes(r.status),
    });
}
