from flask import Flask, request, send_from_directory
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    
    # 获取用户选择的模板
    template_choice = data.get('template_choice', 'default')
    
    # 根据不同模板选择获取相应数据
    if template_choice == 'default':
        # 获取基本信息
        party_a = data.get('party_a', 'Party A')
        party_b = data.get('party_b', 'Party B')
        agreement_content = data.get('agreement_content', 'This is the content of the agreement.')

        # 获取PDF格式设置
        margin = data.get('margin', '2cm')
        linespread = data.get('linespread', '1.5')
        font_size = data.get('font_size', '12pt')

        latex_code = f"""
        \\documentclass[{font_size}]{{article}}
        \\usepackage{{ctex}}
        \\usepackage[utf8]{{inputenc}}
        \\usepackage[margin={margin}]{{geometry}}
        \\usepackage{{setspace}}
        \\setstretch{{{linespread}}}
        \\begin{{document}}
        \\title{{Agreement}}
        \\maketitle

        This Agreement is made this day between {party_a} and {party_b}.

        \\section*{{Terms and Conditions}}
        {agreement_content}

        \\section*{{Signatures}}
        \\noindent
        {party_a}: \\underline{{\\hspace{{4cm}}}} \\hfill {party_b}: \\underline{{\\hspace{{4cm}}}}

        \\end{{document}}
        """
    elif template_choice == 'authorization_letter':
        # 获取受委托书的信息
        client_name = data.get('client_name', '')
        attorney_name = data.get('attorney_name', '')
        work_unit = data.get('work_unit', '')
        position = data.get('position', '')
        phone = data.get('phone', '')
        case_name = data.get('case_name', '')
        case_reason = data.get('case_reason', '')
        agent_power = data.get('agent_power', '')

        latex_code = f"""
        \\documentclass[12pt]{{article}}
        \\usepackage{{ctex}} % 支持中文字符
        \\usepackage{{ulem}} % 用于文本下划线
        \\usepackage{{geometry}} % 页面边距设置
        \\geometry{{a4paper, left=25mm, right=25mm, top=25mm, bottom=25mm}}

        \\begin{{document}}

        \\begin{{center}}
            \\zihao{{3}} \\textbf{{授 权 委 托 书}} % 标题加粗，字号较大
        \\end{{center}}

        \\zihao{{4}} % 正文字号
        \\textbf{{委托人：}} {client_name}\par
        
        \\textbf{{受委托人：}} \\quad 姓名：{attorney_name}\par
        \\hspace*{{27mm}} 工作单位：{work_unit} \\hspace{{2em}} 职务：{position}\par
        \\hspace*{{27mm}} 电话：{phone}\par
        
        现委托上列受委托人在我与{case_name}因{case_reason}纠纷一案中，作为我的诉讼代理人。\par
        
        代理人\\hspace{{2em}}的代理权限为：{agent_power}\par

        \\vspace{{5\\baselineskip}} % 留出五行空白

        \\begin{{flushright}}
            委托人：（签名或盖章）\\underline{{\\hspace{{4cm}}}} \\\\
            年 \\quad 月 \\quad 日
        \\end{{flushright}}

        \\end{{document}}
        """


    elif template_choice == 'legal_rep_identity':
        rep_name = data.get('rep_name', '')
        position = data.get('position', '')
        unit_name = data.get('unit_name', '')
        date = data.get('date', '')
        address = data.get('address', '')
        phone = data.get('phone', '')
        year, month, day = date.split('-')
        
        latex_code = f"""
        \\documentclass[12pt]{{article}}
        \\usepackage{{ctex}} % 支持中文字符
        \\usepackage{{geometry}} % 页面边距设置
        \\geometry{{a4paper, left=25mm, right=25mm, top=25mm, bottom=25mm}}

        \\begin{{document}}

        \\begin{{center}}
            \\zihao{{3}} \\textbf{{法定代表人身份证明书}} % 标题加粗，字号较大
        \\end{{center}}

        \\zihao{{4}} % 正文字号
        \\textbf{{{rep_name}同志，在我单位任{position}职务，特此证明。}} \\

        \\begin{{flushright}}
            \\textbf{{单位全称（盖章）：{unit_name}}} \\\\
            \\textbf{{{year}年 {month}月 {day}日}}
        \\end{{flushright}}
        
        \\vspace{{2\\baselineskip}} % 地址前的空白
        \\textbf{{附：该代表人住址：}}{address} \\

        \\vspace{{1\\baselineskip}} % 地址空白
        \\hspace*{{22mm}} \\textbf{{电 话：{phone}}} \\

        

        \\begin{{flushleft}}
            \\small \\textbf{{注：企业事业单位、机关、团体的主要负责人为本单位的法定代表人。}}
        \\end{{flushleft}}

        \\end{{document}}
        """
    elif template_choice == 'lawyer_agency_contract':
        client_address = data.get('client_address', '')
        client_postcode = data.get('client_postcode', '')
        client_phone = data.get('client_phone', '')
        opponent_name = data.get('opponent_name', '')
        case_reason = data.get('case_reason', '')
        trial_authority = data.get('trial_authority', '')
        trial_level = data.get('trial_level', '')
        dispute_object = data.get('dispute_object', '')

        latex_code = f"""
        \\documentclass[12pt]{{article}}
        \\usepackage{{ctex}} % 支持中文字符
        \\usepackage{{geometry}} % 页面边距设置
        \\geometry{{a4paper, left=25mm, right=25mm, top=25mm, bottom=25mm}}

        \\begin{{document}}

        \\section*{{委托律师代理合同（个人诉讼）}}

        \\subsection*{{甲方信息}}
        \\begin{{itemize}}
            \\item 地址：{client_address}
            \\item 邮政编码：{client_postcode}
            \\item 电话：{client_phone}
        \\end{{itemize}}

        \\subsection*{{乙方信息}}
        乙方：北京市中鸿律师事务所
        \\begin{{itemize}}
            \\item 地址：北京市东长安街 10 号长安大厦 704 室
            \\item 邮政编码：100006
            \\item 电话：010—65251878
            \\item 传真：010—65257668
        \\end{{itemize}}

        甲方因纠纷一案，根据中华人民共和国《合同法》、《民事诉讼法》、《仲裁法》和《律师法》等有关法律的规定，聘请乙方的律师作为委托代理人。

        甲乙双方按照诚实信用原则，经协商一致，立此合同，共同遵守。

        \\section*{{第一条 委托代理事项}}
        乙方接受甲方委托，委派律师在下列案件中担任甲方的委托代理人：
        \\begin{{enumerate}}
            \\item 对方当事人名称或者姓名：{opponent_name}
            \\item 案由：{case_reason}
            \\item 审理机关：{trial_authority}
            \\item 审级：{trial_level}
            \\item 诉讼（仲裁）争议标的：{dispute_object}
        \\end{{enumerate}}

        （此争议标的数额与诉讼/仲裁请求事项均由甲方确定，并对此负责。）

        \\section*{{第二条 委托代理权限}}
        一般代理。
        或者
        特别授权，包括（选择项）：
        \\begin{{enumerate}}
            \\item 变更或者放弃诉讼请求；
            \\item 承认诉讼请求；
            \\item 提起反诉；
            \\item 进行调解或者和解；
            \\item 提起上诉；
            \\item 申请执行；
            \\item 收取或者收转执行标的；
            \\item 签署、送达、接受法律文书。
        \\end{{enumerate}}

        \\section*{{第三条 乙方的义务}}
        \\begin{{enumerate}}
            \\item 乙方委派律师作为上述案件中甲方的委托代理人，甲方同意上述律师指派其他业务助理配合完成辅助工作，但乙方更换代理律师应取得甲方认可；
            \\item 乙方律师应当勤勉、尽责地完成第一条所列委托代理事项；
            \\item 乙方律师应当尽最大努力维护甲方利益；
            \\item 乙方律师应当根据审理机关的要求，及时提交证据，按时出庭，并应甲方要求通报案件进展情况；
            \\item 乙方律师不得违反《律师执业规范》，在涉及甲方的对抗性案件中，未经甲方同意，不得同时担任与甲方具有法律上利益冲突的另一方的委托代理人；
            \\item 乙方律师对其获知的甲方的商业机密／或者甲方的个人隐私负有保密责任，非由法律规定或者甲方同意，不得向任何第三方披露；
            \\item 乙方对涉及甲方的原始证据、法律文件和财物应当妥善保管。
        \\end{{enumerate}}

        \\section*{{第四条 甲方的义务}}
        \\begin{{enumerate}}
            \\item 甲方应当真实、详尽和及时地向乙方律师叙述案件，主动向乙方律师提供与委托代理事项有关的证据、文件及其它事实材料；
            \\item 甲方应当积极、主动地配合乙方律师的工作，甲方对乙方律师提出的要求应当明确、合理；
            \\item 甲方应当按时、足额向乙方支付律师代理费和工作费用；
            \\item 甲方指定为乙方律师的联系人，负责转达甲方的指示和要求，提供文件和资料等；
            \\item 甲方有责任对委托代理事项作出独立的判断、决策。甲方根据乙方律师提供的法律意见、建议、方案所作出的决定而导致的损失，由甲方自行承担；
            \\item 甲方对案件中自己一方的起诉状（仲裁申请）、答辩状、申请书等法律文件的内容、真实、是否有效、是否被有关机关采信负责。
        \\end{{enumerate}}

        \\end{{document}}
        """
    elif template_choice == 'power_of_attorney':
        client_unit = data.get('client_unit', '')
        case = data.get('case', '')
        case_reason = data.get('case_reason', '')
        date = data.get('date', '')
        year, month, day = date.split('-')

        latex_code = f"""
        \\documentclass[12pt]{{article}}
        \\usepackage{{ctex}} % 支持中文字符
        \\usepackage{{geometry}} % 页面边距设置
        \\geometry{{a4paper, left=25mm, right=25mm, top=25mm, bottom=25mm}}

        \\begin{{document}}

        \\section*{{授权委托书}}

        委托单位：{client_unit}

        法定代表人：职务：

        受委托人：姓名：周唯 职务：律师

        工作单位：北京市中闻律师事务所

        住址：北京市海淀区北太平庄路 18 号城建大厦 A 座 7 层

        电话：83355416 手机：13901129159

        现委托上列受委托人在我单位与{case}案，作为我方代理人。 

        因{case_reason}纠纷一

        代理人周唯律师的代理权限为：代理财产保全，代为提出/承认、放弃、变更诉讼请求，进行和解，提起反诉/上诉，参加一/二审诉讼全过程。

        委托单位：{client_unit}

        年 {year} 月 {month} 日 {day}

        \\end{{document}}
        """
    elif template_choice == 'contract':
        
        client_name = data.get('client_name', '')
        client_gender = data.get('client_gender', '')
        client_id = data.get('client_id', '')
        client_phone = data.get('client_phone', '')
        client_email = data.get('client_email', '')
        client_address = data.get('client_address', '')
        opposing_party_name = data.get('opposing_party_name', '')
        case_reason = data.get('case_reason', '')
        judicial_body = data.get('judicial_body', '')
        judicial_level = data.get('judicial_level', '')
        lawyer_fee = data.get('lawyer_fee', '')
        signing_date = data.get('signing_date', '')

        latex_code = f"""
        \\documentclass[12pt]{{article}}
        \\usepackage{{ctex}} % 支持中文字符
        \\usepackage{{geometry}} % 页面边距设置
        \\geometry{{a4paper, left=25mm, right=25mm, top=25mm, bottom=25mm}}

        \\begin{{document}}

        \\section*{{委托代理合同}}

        甲方：\\
        {client_name}\\
        {client_gender}\\
        {client_id}\\
        {client_phone}\\
        {client_email}\\
        {client_address}\\

        乙方：

        根据中华人民共和国相关适用法律，甲方聘请乙方律师作为参加诉讼的委托代理人。双方经协商一致，立此合同。

        \\section{{第一条：委托代理事项}}
        乙方接受甲方委托，委派律师在下列案件中担任甲方的诉讼代理人：\\
        （一）对方当事人名称或者姓名 {opposing_party_name}\\
        （二）案由 {case_reason}\\
        （三）审理机关 {judicial_body}\\
        （四）审级 {judicial_level}\\

        \\section{{第二条 委托代理权限}}
        一般代理。

        \\section{{第三条 乙方义务}}
        "乙方委派赵晶律师作为甲方的委托代理人，代理权限由双方另以《授权委托书》确认。甲方同意乙方委派律师指派其他律师或者业务助理完成除庭审外的委托代理工作。乙方律师应以其依据法律作出的判断，向甲方提示法律风险，尽最大努力维护甲方利益。乙方律师应当根据审理机关的要求，及时提交证据，按时出庭。乙方律师对其获知的甲方信息依法负有保密义务，非由法律规定或者甲方同意，不得向任何第三方披露。"

        \\section{{第四条 甲方义务}}
        "甲方应当真实、详尽和及时地向乙方律师陈述案情，提供与委托代理事项有关的证据、文件及其它事实材料。甲方应当积极、主动配合乙方律师的工作，甲方对乙方律师提出的要求应当明确、合理。甲方应当按时、足额向乙方支付律师费和工作费用。甲方有义务对委托代理事项作出独立的判断、决策。"

        \\section{{第五条 律师费}}
        ¥- {lawyer_fee}（大写：人民币 零 元整）。\\
        甲方于本合同生效之日支付至乙方如下账户：\\
        （一）户 名：\\
        （二）开户行：\\
        （三）账 号：

        \\section{{第六条 工作费用}}
        "乙方律师办理甲方委托代理事项发生的下列工作费用，由甲方承担：（一）相关行政、司法、鉴定、公证等部门收取的费用，包括但不限于乙方为甲方提供法律服务的过程中发生的诉讼费、仲裁费、鉴定费、检验费、评估费、公证费、查档费等；（二）北京市外发生的差旅费、食宿费；（三）征得甲方同意后支出的其它费用。"

        \\section{{第七条 争议解决}}
        因本合同引起的或与本合同有关的任何争议，均适用中华人民共和国法律，并提请北京仲裁委员会／北京国际仲裁中心按照其仲裁规则进行仲裁。仲裁裁决是终局的，对双方均有约束力。

        \\section{{第八条 附则}}
        本合同中文打印，无手书内容，一式三份，甲方一份、乙方二份，由甲方签字、乙方盖章，自签订之日起生效，至乙方完成本合同约定委托代理事项之日终止。

        \\section{{第九条 通知送达}}
        甲乙双方因履行本合同而相互发出或者提供的所有通知、文件、资料，纸质版以双方另行确认的地址送达，电子版以电子邮件送达。电子邮件地址：\\
        （一）甲方： {client_email}\\
        （二）乙方：

        任何一方变更送达地址，应当将变更后的地址送达另一方，否则不得以未送达为由抗辩。
        （下无正文！）

        甲方：\\
        乙方：\\

        “签约日期”于中国北京 {signing_date}

        \\end{{document}}
        """



    
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    tex_filename = 'document.tex'
    pdf_filename = 'document.pdf'
    tex_filepath = os.path.join(output_dir, tex_filename)

    with open(tex_filepath, "w", encoding="utf-8") as file:
        file.write(latex_code)


    # pdflatex_path = "pdflatex"
    # subprocess.run([pdflatex_path, "-output-directory", output_dir, tex_filepath])
    
    # xelatex_path = "xelatex"
    # subprocess.run([xelatex_path, "-output-directory", output_dir, tex_filepath])

    lualatex_path = "lualatex"
    subprocess.run([lualatex_path, "-output-directory", output_dir, tex_filepath])

    return send_from_directory(output_dir, pdf_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
