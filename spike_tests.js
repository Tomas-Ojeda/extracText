import http from 'k6/http';
import { Trend } from 'k6/metrics';
import { check } from 'k6';

const statusTrend = new Trend('status_codes');

export const options = {
    stages: [
        { duration: '10s', target: 50 },  // Rampa de 50 usuarios para prueba estable
        { duration: '20s', target: 50 },
        { duration: '10s', target: 0 },
    ],
    thresholds: {
        http_req_failed: ['rate<0.01'],
        checks: ['rate>0.99'],
        http_req_duration: ['p(95)<3500'],
    },
};

// URL correcta usando el proxy de Traefik
const BASE_URL = 'http://extractext.localhost';

const baseNames = [
    '2020-Scrum-Guide-Spanish-Latin-South-American',
    'Essential-Kanban-Condensed-Spanish',
    'Filosofia Lean',
    'scrum_manager_historias_usuario',
];

// Cargamos un pool controlado de archivos para no saturar memoria/descriptores
const pdfFiles = [];
const pdfNames = [];

for (const base of baseNames) {
    for (let i = 0; i < 3; i++) {
        const name = `${base}_v${i}.pdf`;
        pdfFiles.push(open(`./pdfs_variants/${name}`, 'b'));
        pdfNames.push(name);
    }
}

export default function () {
    const index = Math.floor(Math.random() * pdfFiles.length);
    const randomPdf = pdfFiles[index];
    const dynamicName = `doc_${Date.now()}_${Math.random()}_${pdfNames[index]}`;

    const payload = {
        file: http.file(randomPdf, dynamicName, 'application/pdf'),
    };

    const params = {
        responseType: 'text',
        // Reconoce 200 (duplicado) y 201 (alta nueva) como validos en http_req_failed
        expectedStatuses: [200, 201],
    };

    const res = http.post(`${BASE_URL}/api/v1/documents/`, payload, params);

    statusTrend.add(res.status);

    check(res, {
        'status es 200 o 201': (r) => r.status === 200 || r.status === 201,
        'no es error 500': (r) => r.status !== 500,
    });
}