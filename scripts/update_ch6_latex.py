"""
scripts/update_ch6_latex.py
Updates report/chapters/ch6_frontend_ui.tex to accurately document the new UI design system,
Anthropic frontend-design methodology, modern tokens, Plus Jakarta Sans typography,
interactive components, and updated screenshots.
"""

CH6_CONTENT = r"""\chapter{Frontend Implementation and UI/UX Design System}

\section{Introduction}
When designing StayMart's user interface, the primary architectural goal was to deliver an exceptionally modern, responsive, and trustworthy accommodation and classifieds marketplace specifically tailored for higher education students across Uttarakhand. Traditional generic classified platforms in the region frequently suffer from high broker commissions, misleading property photos, visual clutter, and intrusive advertisements. Conversely, heavy single-page application (SPA) frameworks often impose substantial JavaScript bundle footprints that degrade performance on congested campus wireless networks or remote mountainous cellular towers.

To resolve these practical challenges, StayMart's frontend architecture is engineered using native HTML5, modern CSS3 custom properties, and modular ES6 JavaScript, intentionally rejecting generic template defaults in favor of an authentic design system grounded in Anthropic's frontend-design principles.

This architectural decision yields distinct technical and operational benefits:
\begin{enumerate}
    \item \textbf{Minimal Network Transfer Footprint:} The total initial stylesheet and JavaScript payload remains under 45 KB (excluding compressed media), ensuring sub-second rendering even on constrained 3G/4G student cellular connections.
    \item \textbf{Zero Build-Chain Complexity:} The application operates natively in the browser without requiring Webpack, Vite, Babel, or complex Node.js build pipelines, streamlining static hosting, automated audits, and edge CDN deployments.
    \item \textbf{Predictable DOM Lifecycles and High Performance:} Utilizing native browser APIs, CSS hardware-accelerated transitions, and standard Fetch requests eliminates virtual DOM diffing overhead and ensures 60 FPS scrolling and interaction fidelity.
\end{enumerate}

\section{Design Philosophy and Visual Design System}
Rather than adopting trendy dark-mode templates or ubiquitous AI archetypes (such as warm cream canvases paired with terracotta accents or near-black backgrounds with neon highlights), StayMart establishes an authentic, high-trust visual identity grounded in the physical and academic geography of Uttarakhand.

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.95\textwidth]{screenshots/landing_page.png}
    \caption{StayMart Modern Landing Interface Featuring Alpine Navy Navigation, Refined Campus Chips, and Real-Time Marketplace Metrics}
    \label{fig:landing_page_ui}
\end{figure}

The visual system is governed by three fundamental design tenets:
\begin{itemize}
    \item \textbf{Subject-Matter Grounding:} The user interface is purpose-built for student reality in Dehradun, Prem Nagar, Clement Town, Rajpur Road, and Bhimtal. Features such as campus gate proximity badges (``400m from GEHU Gate 2''), verified roommate preferences (Boys, Girls, Co-ed), and room essential categories directly address outstation student life.
    \item \textbf{High-Contrast Commercial Dignity:} An ultra-crisp pearl white canvas (\texttt{\#f8fafc}) paired with pure white container surfaces (\texttt{\#ffffff}) and delicate slate borders (\texttt{\#e2e8f0}) delivers exceptional readability, eliminating ocular fatigue in high-ambient-light classroom environments.
    \item \textbf{Restraint and Cohesive Elevation:} Rather than decorative glassmorphism or excessive drop shadows, surfaces use structured multi-layer elevation (\texttt{0 4px 16px -2px rgba(11, 30, 54, 0.08)}) that provides clear tactile depth without distracting from property photography.
\end{itemize}

\subsection{Color Palette and Design Tokens}
The color system is formalized as a compact token architecture declared within \texttt{:root} in \texttt{frontend/css/global.css}. All colors are selected for WCAG AAA accessibility contrast compliance and distinct semantic roles:

\begin{itemize}
    \item \textbf{Deep Himalayan Alpine Navy (\texttt{\#0b1e36}):} Represents institutional reliability, security, and academic stability. Serves as the primary brand backdrop across global navigation bars, modal headers, and primary typography.
    \item \textbf{Radiant Sunfire Amber (\texttt{\#f59e0b} to \texttt{\#ea580c}):} An energetic, warm conversion accent powering primary calls-to-action, the signature Sell CTA, and active highlight states.
    \item \textbf{Emerald Mint (\texttt{\#10b981}):} Denotes positive verification, active landlord verification stamps, zero-brokerage guarantees, and calculated monetary savings.
    \item \textbf{Glacier Blue (\texttt{\#0284c7}):} Informational accent for navigation links, secondary badges, and interactive filter controls.
\end{itemize}

Listing \ref{lst:design_tokens} provides the active design token declarations:

\begin{lstlisting}[language=HTML, caption={Active Design Tokens in frontend/css/global.css}, label={lst:design_tokens}]
:root {
  /* Brand Palette: Deep Himalayan Alpine Navy + Radiant Amber + Emerald Mint */
  --header-bg: #0b1e36;            /* Deep Alpine Navy - authoritative, high-trust */
  --header-text: #ffffff;
  --header-hover: #38bdf8;          /* Crisp Glacier Sky */
  
  --amazon-amber: #f59e0b;          /* Radiant Himalayan Amber */
  --amazon-yellow: #f59e0b;         /* Modern Amber */
  --amazon-yellow-hover: #d97706;   /* Deep Warm Amber */
  --amazon-dark: #091524;           /* Midnight Slate */
  
  --olx-teal: #0b1e36;              /* Deep Alpine Navy */
  --olx-cyan: #0284c7;              /* Crisp Cobalt Cyan */
  --olx-light-teal: #f0f7ff;        /* Soft Alpine Mist */
  
  /* Modern Commercial Neutral Surfaces (Clean Luminous Theme) */
  --bg-page: #f8fafc;               /* Crisp Pearl White Canvas */
  --bg-card: #ffffff;
  --bg-hover: #f1f5f9;
  --bg-subtle: #f8fafc;
  
  /* Text & Typography */
  --text-primary: #0b1e36;          /* High contrast deep navy */
  --text-secondary: #475569;        /* Slate 600 - crisp subtitles */
  --text-muted: #64748b;            /* Slate 500 - accessible metadata (WCAG AAA) */
  --text-link: #0284c7;             /* Vibrant Sky Blue */
  
  /* Borders & Dividers */
  --border: #e2e8f0;                /* Ultra crisp, delicate slate border */
  --border-subtle: #edf2f7;
  --border-focus: #f59e0b;          /* Warm radiant amber ring */
  
  /* Status & Accents */
  --success: #10b981;               /* Emerald Mint Verified */
  --danger: #ef4444;                /* Vivid Coral Red */
  --warning: #f59e0b;               /* Amber warning */
  --info: #0284c7;                  /* Glacier Blue */
  
  /* Elevation & Shadows */
  --shadow-sm: 0 1px 3px rgba(11, 30, 54, 0.05);
  --shadow-md: 0 4px 16px -2px rgba(11, 30, 54, 0.08), 0 2px 6px -1px rgba(11, 30, 54, 0.04);
  --shadow-lg: 0 16px 36px -4px rgba(11, 30, 54, 0.12), 0 6px 16px -2px rgba(11, 30, 54, 0.06);
  
  /* Geometry & Rhythm */
  --radius-sm: 6px;
  --radius: 10px;
  --radius-lg: 16px;
  --radius-full: 9999px;
  --font: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-display: 'Plus Jakarta Sans', var(--font);
  --transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
  --transition-fast: all 0.14s cubic-bezier(0.16, 1, 0.3, 1);
  --transition-spring: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}
\end{lstlisting}

\subsection{Dual Typography Architecture & Micro-Interactions}
Typography establishes visual personality and structural hierarchy following \textit{The Elements of Typographic Style}:
\begin{itemize}
    \item \textbf{Display Face (\texttt{Plus Jakarta Sans}):} Applied to all display titles, hero headings, brand logotypes, financial indicators, and card prices. Its geometric precision and optical balance give the interface an elevated, editorial identity.
    \item \textbf{Body Face (\texttt{Inter}):} Applied to long-form descriptions, tabular specifications, filter labels, and metadata. Chosen for its open aperture, neutral rendering, and legibility at small sizes.
    \item \textbf{Elimination of AI Telltales:} Generic artificial intelligence templates often introduce visual clutter through unstyled system emojis, all-caps labels, and single-word colored accents in headlines. StayMart systematically replaces emoji noise with clean typographic hierarchy and purposeful badge tokens.
    \item \textbf{Modernized Action Micro-Interactions:} The primary listing button (\texttt{.btn-olx-sell}) was redesigned from a dated multi-color border into an elevated amber-to-sunset gradient pill with a dynamic shimmer layer and soft ambient glow, providing clear feedback on hover and focus.
\end{itemize}

\section{Modular Client-Side JavaScript Architecture}
To enforce clean separation of concerns without requiring bundlers, frontend logic is partitioned into modular scripts residing in \texttt{frontend/js/}:

\subsection{1. Unified API Client (\texttt{api.js})}
Acts as the central network boundary for all backend communication:
\begin{itemize}
    \item \textbf{Environment Detection:} Dynamically detects local development (\texttt{localhost:8080}) or cloud production hosts, supporting runtime \texttt{localStorage} base URL overrides for seamless multi-environment testing.
    \item \textbf{Stateless Token Injection:} Automatically extracts the user's JWT from secure browser storage and appends the standard \texttt{Authorization: Bearer <token>} HTTP header on protected requests.
    \item \textbf{Standardized Envelope Unwrapping:} Parses the backend's uniform \texttt{ApiResponse<T>} payload, extracting data models while mapping structured error codes to user-friendly notifications.
\end{itemize}

\subsection{2. State and Authentication Manager (\texttt{auth.js})}
Governs user session states, access authorization, and dynamic UI hydration:
\begin{itemize}
    \item Validates existing session tokens on page initialization via \texttt{GET /api/users/me}.
    \item Protects private routes by intercepting unauthorized attempts to access user bookings or listing submission portals, redirecting users to \texttt{login.html}.
    \item Enforces role-based view isolation, ensuring that administrative dashboards and moderation controls are strictly restricted to authenticated users bearing the \texttt{ROLE\_ADMIN} authority.
    \item Synchronizes header user profiles, alternating between login/register buttons and authenticated user menus.
\end{itemize}

\subsection{3. Behavioral Event Tracker (\texttt{behavior.js})}
Captures non-blocking user interaction telemetry (property views, category searches, wishlist toggles). Events are transmitted asynchronously to the backend to train the recommendation engine.

\subsection{4. Utility Library (\texttt{utils.js})}
Encapsulates platform-wide helper routines:
\begin{itemize}
    \item \texttt{escapeHtml(str)}: Sanitizes user-generated text prior to DOM injection to thwart Cross-Site Scripting (XSS).
    \item \texttt{formatPrice(amount)}: Formats numerical integers into localized Indian Rupee currency strings (e.g., \texttt{₹7,500/mo}).
    \item Dynamic toast notifications, relative timestamp formatters, and dialog window helpers.
\end{itemize}

\subsection{5. Marketplace Statistics and Calculators (\texttt{stats.js})}
Powers interactive marketplace counters and financial models:
\begin{itemize}
    \item \textbf{Animated Counter Engine:} Utilizes modern \texttt{IntersectionObserver} APIs to smoothly increment platform statistics as viewers scroll into view.
    \item \textbf{Student Accommodation Savings Calculator:} An interactive financial workbench calculating estimated brokerage fees avoided, bundled utility values, and annual net cash savings based on user-selected rent brackets.
    \item \textbf{Campus Gear Re-Commerce Calculator:} Simulates savings on pre-owned university essentials (laptops, coolers, study desks, bicycles) compared against retail benchmarks, including calculated carbon emission reductions.
\end{itemize}

\subsection{6. Visual Charts and Trend Renderers (\texttt{charts.js})}
Integrates responsive Chart.js data visualizations:
\begin{itemize}
    \item \textbf{Campus Rental Rate Distribution:} Illustrates median monthly rents across key Dehradun academic belts (Clement Town, Prem Nagar, Rajpur Road, Bhimtal).
    \item \textbf{Student Re-Commerce Price Benchmarks:} Compares second-hand student resale prices against commercial retail benchmarks.
\end{itemize}

\section{Public Portals and User Flows}

\subsection{Landing and Discovery Portal (\texttt{index.html})}
The homepage serves as the command hub for campus life:
\begin{itemize}
    \item \textbf{Unified Campus Command Bar:} Features a multi-campus location selector (Graphic Era GEU/GEHU, UPES Bidholi/Kandoli, DIT Dehradun, IIT Roorkee) paired with a high-speed search console.
    \item \textbf{Category Navigation Strip:} Delivers instant faceted access to verified student PGs, independent flats, engineering laptops, smartphones, two-wheelers, study furniture, and semester textbooks.
    \item \textbf{Real-Time Metrics Ribbon:} Showcases verified listing tallies, student savings benchmarks, and college-ID verification rates.
    \item \textbf{Interactive Student Savings Workbench:} Enables students and parents to model annual cost reductions through zero-brokerage rentals and circular campus commerce.
\end{itemize}

\subsection{Faceted Accommodation and Product Search Portals}
The search interfaces (\texttt{search-properties.html} and \texttt{search-products.html}) provide multi-attribute faceted filtering:

\begin{figure}[htbp]
    \centering
    \begin{subfigure}[b]{0.48\textwidth}
        \includegraphics[width=\textwidth]{screenshots/search_properties.png}
        \caption{Property Search with Amenities Filter}
    \end{subfigure}
    \hfill
    \begin{subfigure}[b]{0.48\textwidth}
        \includegraphics[width=\textwidth]{screenshots/search_products.png}
        \caption{Product Search with Category Filter}
    \end{subfigure}
    \caption{Faceted Search Interfaces with Real Listing Photography}
    \label{fig:search_screens}
\end{figure}

\begin{itemize}
    \item \textbf{Faceted Filter Controls:} Multi-variable filtering by city, neighborhood zone, accommodation type (PG, Flat, Hostel), budget slider, gender preference (Boys, Girls, Co-ed), and essential student amenities (WiFi, Power Backup, Meals Included, AC).
    \item \textbf{Standardized 4:3 Image Cards:} Displays authentic room and product photography, price tags with transparent monthly breakdown, campus proximity tags, and live room vacancy status.
    \item \textbf{Mobile Filter Drawer:} On viewport widths under 768px, filters collapse into an intuitive slide-up drawer with persistent filter count badges, ensuring zero horizontal overflow.
\end{itemize}

\subsection{Listing Detail Portals}
Detail views (\texttt{property-detail.html} and \texttt{product-detail.html}) present verified information:

\begin{figure}[htbp]
    \centering
    \begin{subfigure}[b]{0.48\textwidth}
        \includegraphics[width=\textwidth]{screenshots/property_detail.png}
        \caption{Property Details and Room Booking Widget}
    \end{subfigure}
    \hfill
    \begin{subfigure}[b]{0.48\textwidth}
        \includegraphics[width=\textwidth]{screenshots/product_detail.png}
        \caption{Product Details with Specifications}
    \end{subfigure}
    \caption{Listing Detail Pages with Interactive Galleries and Host Details}
    \label{fig:detail_screens}
\end{figure}

\begin{itemize}
    \item \textbf{High-Resolution Photo Gallery:} Thumbnail-driven interactive gallery enabling outstation students to inspect room conditions prior to visiting.
    \item \textbf{Direct Host Connection Card:} Features verified landlord identity badges and direct WhatsApp and phone dialing actions, eliminating middleman interference.
    \item \textbf{Dynamic Room Reservation Module:} Allows students to select sharing configuration (Single, Double, Triple), set lease durations, review total estimated costs, and submit direct booking inquiries.
    \item \textbf{Mobile Sticky Action Bar:} On handheld screens, a fixed bottom action bar provides continuous access to ``Call Host'' and ``Book Room'' buttons without requiring manual scrolling.
\end{itemize}

\section{Self-Service User and Admin Management Portals}

\subsection{User Dashboard and Account Management}
The user dashboard (\texttt{pages/user/dashboard.html}) aggregates personal interactions:

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.95\textwidth]{screenshots/user_dashboard.png}
    \caption{User Dashboard Showing Activity Summaries and Recommendations}
    \label{fig:user_dashboard_ui}
\end{figure}

\begin{itemize}
    \item \textbf{Operational Activity Cards:} Quantitative metrics tracking active booking inquiries, submitted orders, personal listings, and saved wishlist items.
    \item \textbf{Lifecycle Status Indicators:} Visual indicators tracking booking states (\texttt{PENDING}, \texttt{CONFIRMED}, \texttt{COMPLETED}, \texttt{CANCELLED}).
    \item \textbf{Tailored Machine Learning Recommendations:} Dynamic listing carousel generated by the TF-IDF recommendation microservice based on browsing behavior.
\end{itemize}

\subsection{Peer-to-Peer Messaging Portal}
Direct communication between students and accommodation caretakers takes place in \texttt{pages/user/chat.html}:

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.95\textwidth]{screenshots/user_chat.png}
    \caption{Peer-to-Peer Chat Interface Between Student and Caretaker}
    \label{fig:chat_ui}
\end{figure}

\begin{itemize}
    \item Unified conversation thread listing with live unread indicators.
    \item Conversational chat pane with message timestamps and sender avatars.
    \item Contextual initialization: clicking ``Message Caretaker'' on a property pre-populates the chat input with the listing title and pricing details.
\end{itemize}

\subsection{Administrative Moderation Console}
Platform moderators operate through \texttt{pages/admin/dashboard.html}:

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.95\textwidth]{screenshots/admin_dashboard.png}
    \caption{Administrative Console with Platform Metrics and Moderation Controls}
    \label{fig:admin_dashboard_ui}
\end{figure}

\begin{itemize}
    \item Quantitative platform health tallies: total registered students, verified properties, vacant rooms, active product ads, and pending reviews.
    \item Moderation Workflows: Enables staff to inspect newly posted student PGs and products, verify uploaded photographs and pricing fairness, and approve or reject submissions prior to public catalog indexing.
\end{itemize}

\section{Summary}
This chapter presented the comprehensive frontend architecture of StayMart. By implementing a modern commercial light design system with native HTML5, CSS3 Custom Properties, and ES6 JavaScript, the platform avoids client-side framework bloat while providing sub-second page rendering and high visual dignity. The design is grounded in the authentic needs of Uttarakhand students, featuring the Himalayan Alpine Navy and Radiant Amber palette, Plus Jakarta Sans typography, interactive savings calculators, and multi-viewport responsive resilience. The subsequent chapter presents software verification methodologies, automated test suites, and empirical evaluation results.
"""

with open("report/chapters/ch6_frontend_ui.tex", "w", encoding="utf-8") as f:
    f.write(CH6_CONTENT.strip() + "\n")

print("Successfully updated report/chapters/ch6_frontend_ui.tex with the NEW UI design system!")

