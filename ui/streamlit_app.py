# import json

# import streamlit as st

# from app.service import (
#     analyze_project_dependencies,
#     report_to_dict
# )


# st.set_page_config(
#     page_title="AI Dependency Upgrade Agent",
#     page_icon="🔍",
#     layout="wide"
# )


# st.title("AI Dependency Upgrade & Compatibility Agent")

# st.write(
#     "Analyze a Python project before upgrading its dependencies."
# )


# st.sidebar.header("Project Settings")

# project_path = st.sidebar.text_input(
#     "Project Path",
#     value="sample_project"
# )

# run_tests = st.sidebar.checkbox(
#     "Run Tests",
#     value=True
# )

# analyze_button = st.sidebar.button(
#     "Analyze Project"
# )


# if analyze_button:

#     with st.spinner("Analyzing project..."):

#         try:
#             report = analyze_project_dependencies(
#                 project_path=project_path,
#                 run_project_tests=run_tests
#             )

#             st.session_state["report"] = report

#         except Exception as exc:
#             st.error(
#                 f"Analysis failed: {exc}"
#             )


# if "report" in st.session_state:

#     report = st.session_state["report"]

#     st.success("Analysis completed.")

#     st.subheader("Risk Summary")

#     col1, col2 = st.columns(2)

#     with col1:
#         st.metric(
#             "Risk Level",
#             report.risk_level
#         )

#     with col2:
#         st.metric(
#             "Risk Score",
#             report.risk_score
#         )

#     st.subheader("Dependency Analysis")

#     dependency_data = []

#     for dependency in report.dependencies:
#         dependency_data.append(
#             {
#                 "Package": dependency.name,
#                 "Current": dependency.current_version,
#                 "Latest": dependency.latest_version,
#                 "Update Available": dependency.update_available,
#                 "Error": dependency.error
#             }
#         )

#     st.dataframe(
#         dependency_data,
#         use_container_width=True
#     )

#     st.subheader("Code Compatibility Findings")

#     if report.code_findings:

#         finding_data = []

#         for finding in report.code_findings:
#             finding_data.append(
#                 {
#                     "File": finding.file,
#                     "Line": finding.line,
#                     "Severity": finding.severity,
#                     "Issue": finding.issue,
#                     "Suggestion": finding.suggestion
#                 }
#             )

#         st.dataframe(
#             finding_data,
#             use_container_width=True
#         )

#     else:
#         st.info(
#             "No compatibility findings detected."
#         )

#     st.subheader("Test Results")

#     if report.test_result:

#         col1, col2, col3 = st.columns(3)

#         with col1:
#             st.metric(
#                 "Passed",
#                 report.test_result.passed
#             )

#         with col2:
#             st.metric(
#                 "Failed",
#                 report.test_result.failed
#             )

#         with col3:
#             st.metric(
#                 "Skipped",
#                 report.test_result.skipped
#             )

#         with st.expander("View Test Output"):
#             st.code(
#                 report.test_result.output
#             )

#     else:
#         st.info(
#             "Tests were not executed."
#         )

#     st.subheader("Retrieved Documentation")

#     if report.documentation:

#         for index, document in enumerate(
#             report.documentation,
#             start=1
#         ):

#             with st.expander(
#                 f"Document {index}"
#             ):
#                 st.markdown(document)

#     else:
#         st.info(
#             "No relevant documentation found."
#         )

#     st.subheader("AI Engineering Assessment")

#     if report.ai_analysis:
#         st.markdown(report.ai_analysis)

#     else:
#         st.info(
#             "Gemini analysis is unavailable. "
#             "Add GEMINI_API_KEY to enable it."
#         )

#     st.subheader("Export Report")

#     report_json = json.dumps(
#         report_to_dict(report),
#         indent=4
#     )

#     st.download_button(
#         label="Download JSON Report",
#         data=report_json,
#         file_name="upgrade_report.json",
#         mime="application/json"
#     )


import json

import streamlit as st

from app.service import (
    analyze_project_dependencies,
    report_to_dict
)


st.set_page_config(
    page_title="AI Dependency Upgrade Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown(
    """
    <style>
        .stApp {
            background: #f6f8fb;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .hero {
            background: linear-gradient(
                135deg,
                #111827 0%,
                #1e3a5f 55%,
                #2563eb 100%
            );
            padding: 2.2rem 2.5rem;
            border-radius: 20px;
            color: white;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.10);
        }

        .hero h1 {
            margin: 0;
            font-size: 2.3rem;
            font-weight: 700;
        }

        .hero p {
            margin-top: 0.7rem;
            margin-bottom: 0;
            font-size: 1rem;
            opacity: 0.88;
        }

        .section-title {
            font-size: 1.35rem;
            font-weight: 650;
            margin-top: 1.3rem;
            margin-bottom: 0.8rem;
            color: #172033;
        }

        .info-card {
            background: white;
            border: 1px solid #e5eaf0;
            border-radius: 16px;
            padding: 1.2rem 1.4rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
        }

        .pipeline {
            display: flex;
            gap: 0.6rem;
            flex-wrap: wrap;
            margin: 1rem 0 1.5rem 0;
        }

        .pipeline-item {
            background: white;
            border: 1px solid #e3e8ef;
            border-radius: 12px;
            padding: 0.65rem 0.9rem;
            color: #334155;
            font-size: 0.88rem;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
        }

        .pipeline-arrow {
            color: #94a3b8;
            align-self: center;
        }

        .risk-card {
            background: white;
            border: 1px solid #e5eaf0;
            border-radius: 16px;
            padding: 1.1rem 1.3rem;
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
        }

        .card-label {
            color: #64748b;
            font-size: 0.85rem;
            margin-bottom: 0.35rem;
        }

        .card-value {
            color: #111827;
            font-size: 1.55rem;
            font-weight: 700;
        }

        .status-badge {
            display: inline-block;
            padding: 0.35rem 0.7rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 650;
            margin-top: 0.3rem;
        }

        .status-medium {
            background: #fff7ed;
            color: #c2410c;
        }

        .status-high {
            background: #fef2f2;
            color: #b91c1c;
        }

        .status-low {
            background: #ecfdf5;
            color: #047857;
        }

        .ai-card {
            background: white;
            border: 1px solid #e5eaf0;
            border-radius: 18px;
            padding: 1.6rem 1.8rem;
            box-shadow: 0 5px 20px rgba(15, 23, 42, 0.05);
            margin-top: 0.5rem;
        }

        .ai-heading {
            font-size: 1.15rem;
            font-weight: 650;
            color: #172033;
            margin-bottom: 1rem;
        }

        .sidebar-note {
            background: #eff6ff;
            border: 1px solid #dbeafe;
            border-radius: 12px;
            padding: 0.8rem;
            color: #1e40af;
            font-size: 0.82rem;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 14px;
            overflow: hidden;
        }

        div[data-testid="stExpander"] {
            border-radius: 12px;
            border: 1px solid #e5eaf0;
        }

        .footer {
            text-align: center;
            color: #94a3b8;
            font-size: 0.8rem;
            padding-top: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="hero">
        <h1>🔍 AI Dependency Upgrade Agent</h1>
        <p>
            Analyze dependency upgrades, detect compatibility issues,
            evaluate project health, and generate AI-powered migration guidance.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


st.sidebar.title("Project Settings")

st.sidebar.markdown(
    """
    <div class="sidebar-note">
        Select a Python project and run the compatibility analysis.
        The report combines dependency checks, source analysis,
        testing, RAG retrieval, and Gemini.
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.write("")

project_path = st.sidebar.text_input(
    "Project Path",
    value="sample_project"
)

run_tests = st.sidebar.checkbox(
    "Run Tests",
    value=True
)

analyze_button = st.sidebar.button(
    "🚀 Analyze Project",
    use_container_width=True
)


if analyze_button:

    with st.spinner(
        "Analyzing dependencies, source code, tests, and documentation..."
    ):

        try:
            report = analyze_project_dependencies(
                project_path=project_path,
                run_project_tests=run_tests
            )

            st.session_state["report"] = report

        except Exception as exc:
            st.error(
                f"Analysis failed: {exc}"
            )


if "report" in st.session_state:

    report = st.session_state["report"]

    st.success("Analysis completed successfully.")

    st.markdown(
        """
        <div class="pipeline">
            <div class="pipeline-item">📦 Dependencies</div>
            <div class="pipeline-arrow">→</div>
            <div class="pipeline-item">🔎 Source Analysis</div>
            <div class="pipeline-arrow">→</div>
            <div class="pipeline-item">🧪 Tests</div>
            <div class="pipeline-arrow">→</div>
            <div class="pipeline-item">⚠️ Risk Scoring</div>
            <div class="pipeline-arrow">→</div>
            <div class="pipeline-item">📚 RAG</div>
            <div class="pipeline-arrow">→</div>
            <div class="pipeline-item">🤖 Gemini</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    risk_level = report.risk_level.upper()

    if risk_level == "HIGH":
        risk_class = "status-high"
    elif risk_level == "MEDIUM":
        risk_class = "status-medium"
    else:
        risk_class = "status-low"

    st.markdown(
        '<div class="section-title">Project Overview</div>',
        unsafe_allow_html=True
    )

    st.caption(
        f"Analyzed project: {report.project_path}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="risk-card">
                <div class="card-label">Risk Level</div>
                <div class="card-value">{risk_level}</div>
                <span class="status-badge {risk_class}">
                    {risk_level} RISK
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="risk-card">
                <div class="card-label">Risk Score</div>
                <div class="card-value">{report.risk_score}</div>
                <div class="card-label">
                    Based on dependencies, code findings and tests
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="risk-card">
                <div class="card-label">Dependencies</div>
                <div class="card-value">{len(report.dependencies)}</div>
                <div class="card-label">
                    Packages analyzed
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="section-title">Analysis Details</div>',
        unsafe_allow_html=True
    )

    (
        overview_tab,
        dependency_tab,
        code_tab,
        test_tab,
        rag_tab,
        ai_tab,
        report_tab
    ) = st.tabs(
        [
            "Overview",
            "Dependencies",
            "Code Findings",
            "Tests",
            "RAG Knowledge",
            "AI Assessment",
            "JSON Report"
        ]
    )

    with overview_tab:

        st.markdown(
            """
            <div class="info-card">
                <strong>What this analysis checks</strong><br>
                The agent combines dependency version analysis,
                source-code inspection, automated testing,
                risk scoring, retrieved documentation, and
                AI-generated engineering recommendations.
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:

            update_count = sum(
                1
                for dependency in report.dependencies
                if dependency.update_available
            )

            st.metric(
                "Updates Available",
                update_count
            )

        with col2:

            st.metric(
                "Code Findings",
                len(report.code_findings)
            )

    with dependency_tab:

        st.write(
            "Current package versions compared with the latest versions found on PyPI."
        )

        dependency_data = []

        for dependency in report.dependencies:
            dependency_data.append(
                {
                    "Package": dependency.name,
                    "Current": dependency.current_version,
                    "Latest": dependency.latest_version,
                    "Update Available": dependency.update_available,
                    "Error": dependency.error
                }
            )

        if dependency_data:
            st.dataframe(
                dependency_data,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No dependencies were found.")

    with code_tab:

        if report.code_findings:

            finding_data = []

            for finding in report.code_findings:
                finding_data.append(
                    {
                        "File": finding.file,
                        "Line": finding.line,
                        "Severity": finding.severity,
                        "Issue": finding.issue,
                        "Suggestion": finding.suggestion
                    }
                )

            st.dataframe(
                finding_data,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.success(
                "No compatibility findings were detected."
            )

    with test_tab:

        if report.test_result:

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Passed",
                    report.test_result.passed
                )

            with col2:
                st.metric(
                    "Failed",
                    report.test_result.failed
                )

            with col3:
                st.metric(
                    "Skipped",
                    report.test_result.skipped
                )

            with col4:
                st.metric(
                    "Return Code",
                    report.test_result.return_code
                )

            with st.expander(
                "View Test Output"
            ):
                st.code(
                    report.test_result.output,
                    language="text"
                )

        else:
            st.info("Tests were not executed.")

    with rag_tab:

        st.write(
            "Relevant documents retrieved from the project's knowledge base."
        )

        if report.documentation:

            for index, document in enumerate(
                report.documentation,
                start=1
            ):

                with st.expander(
                    f"📄 Retrieved Document {index}"
                ):
                    st.markdown(document)

        else:
            st.info(
                "No relevant documentation was retrieved."
            )

    with ai_tab:

        st.markdown(
            """
            <div class="ai-card">
                <div class="ai-heading">
                    🤖 AI Engineering Assessment
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if report.ai_analysis:
            st.markdown(report.ai_analysis)
        else:
            st.warning(
                "Gemini analysis is unavailable. "
                "Add GEMINI_API_KEY to enable AI analysis."
            )

    with report_tab:

        st.write(
            "Machine-readable report generated by the analysis pipeline."
        )

        report_data = report_to_dict(report)

        st.json(report_data)

        report_json = json.dumps(
            report_data,
            indent=4
        )

        st.download_button(
            label="⬇️ Download JSON Report",
            data=report_json,
            file_name="upgrade_report.json",
            mime="application/json",
            use_container_width=True
        )


else:

    st.markdown(
        """
        <div class="info-card">
            <strong>Ready to analyze</strong><br><br>
            Enter the path of a Python project in the sidebar
            and click <strong>Analyze Project</strong>.
            The dashboard will display dependency updates,
            compatibility findings, test results, retrieved
            documentation, and the AI engineering assessment.
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    """
    <div class="footer">
        AI Dependency Upgrade & Compatibility Agent
        • Python • AST • PyPI • pytest • RAG • Gemini
    </div>
    """,
    unsafe_allow_html=True
)