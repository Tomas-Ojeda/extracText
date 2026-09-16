import http from 'k6/http';
import { Trend } from 'k6/metrics';
import { check } from 'k6';

const statusTrend = new Trend('status_codes');

export const options = {
    stages: [
        { duration: '10s', target: 100 },
        { duration: '20s', target: 100 },
        { duration: '10s', target: 0 },
    ],
};

const BASE_URL = 'http://extractext.localhost';

// Carga de PDFs en modo binario durante la inicialización (init context de k6)
const pdfFiles = [
    open('./pdfs/2020-Scrum-Guide-Spanish-Latin-South-American.pdf', 'b'),
    open('./pdfs/Essential-Kanban-Condensed-Spanish.pdf', 'b'),
    open('./pdfs/Filosofia Lean.pdf', 'b'),
    open('./pdfs/scrum_manager_historias_usuario.pdf', 'b'),
];

const pdfNames = [
    '2020-Scrum-Guide-Spanish-Latin-South-American.pdf',
    'Essential-Kanban-Condensed-Spanish.pdf',
    'Filosofia Lean.pdf',
    'scrum_manager_historias_usuario.pdf',
];

export default function () {
    // Selección aleatoria de un PDF de la lista
    const index = Math.floor(Math.random() * pdfFiles.length);
    const randomPdf = pdfFiles[index];
    const randomName = pdfNames[index];

    // El endpoint real es /api/v1/documents/ y espera multipart/form-data
    // con un campo "file" (ver openapi.json del proyecto)
    const payload = {
        file: http.file(randomPdf, randomName, 'application/pdf'),
    };

    const res = http.post(`${BASE_URL}/api/v1/documents/`, payload);

    statusTrend.add(res.status);

    check(res, {
        'status 201': (r) => r.status === 201,
    });
}
