# Python을 이용한 실시간 공정 모니터링 시스템

<img src="https://github.com/doney0222/PLC_monitoring_system/img/image01.png">

## 프로젝트의 목적

- 스마트팩토리 관련 교육을 받는 학생들이 쉽게 이용할 수 있는 공정 모니터링 시스템 제작
- 공정 작동 중 이상상황 발생시 즉시 관리자에게 알림을 보내는 이상알림 기능 제작

## 개발 환경

- 운영체제 : Windows 10
- PC 프로그래밍 : Visual Studio Code
- PLC 프로그래밍 : Sysmac Studio
- 사용언어 : Python

## 기능

- 소켓 통신을 이용한 PLC 데이터 수집
- 멀티스레드 적용을 통한 다중 PLC 연결 및 데이터 송수신
- 데이터 베이스 연동을 통한 데이터 축적
- 간편한 모니터링 UI
- 그래프를 이용한 데이터 출력
- 이상상황 발생시 OpenAPI를 이용한 카카오톡 메시지 전송
- 이상상황 발생시 OpenAPI를 이용한 네이버 메일 전송

