// Version reducida SOLO para iteración rápida / diagnóstico.
import http from 'k6/http';
import { Trend } from 'k6/metrics';
import { check } from 'k6';

const statusTrend = new Trend('status_codes');

export const options = {
    stages: [
        { duration: '5s', target: 30 },
        { duration: '5s', target: 30 },
        { duration: '5s', target: 0 },
    ],
};

const BASE_URL = 'http://extractext.localhost';

const baseNames = [
    '2020-Scrum-Guide-Spanish-Latin-South-American',
    'Essential-Kanban-Condensed-Spanish',
    'Filosofia Lean',
    'scrum_manager_historias_usuario',
];

// Limitar a 3 variantes por base para evitar colapsar descriptores en Windows (12 archivos en total)
const VARIANTS_PER_FILE = 3;

const pdfFiles = [];
const pdfNames = [];

for (const base of baseNames) {
    for (let i = 0; i < VARIANTS_PER_FILE; i++) {
        const name = `${base}_v${i}.pdf`;
        pdfFiles.push(open(`./pdfs_variants/${name}`, 'b'));
        pdfNames.push(name);
    }
}

export default function () {
    const index = Math.floor(Math.random() * pdfFiles.length);
    const randomPdf = pdfFiles[index];
    const randomName = pdfNames[index];

    const payload = {
        file: http.file(randomPdf, randomName, 'application/pdf'),
    };

    const params = { 
        timeout: '90s',
        // Evita falsos fallos en la metrica http_req_failed cuando la API devuelve 409
        expectedStatuses: [201, 409],
    };

    const res = http.post(`${BASE_URL}/api/v1/documents/`, payload, params);

    statusTrend.add(res.status);

    check(res, {
        'status es 201 o 409 (esperado)': (r) => r.status === 201 || r.status === 409,
        'no es error 500': (r) => r.status !== 500,
    });
}